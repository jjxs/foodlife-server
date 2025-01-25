
import datetime
from urllib import request
from zipfile import is_zipfile

from botocore import model
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
import app.util as Util
from app.db.models.store_table import (
    AuthGroup, AuthUserGroups, AuthMenu, Machine)
from app.exception.web import WebException
from app.http.api import BaseAPI
from app.http.response import JsonResponse

UserModel = get_user_model()


class UserGroupApi(BaseAPI):

    def get_group_data(self, request, params):
        '''グループデータ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            id,
            name
        FROM
            auth_group
        WHERE 1 = 1
            {0}
        ORDER BY
            id
        '''

        if 'keyword' in params and params['keyword']:
            sql_condition.append(
                ' AND (name LIKE %(keyword)s)'
            )
            sql_param['keyword'] = '%' + params['keyword'] + '%'

        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_list(sql=sql, params=sql_param, DB_name=DATA_BASE)

        sql = '''
            SELECT 
                AUG.user_id,
                AUG.group_id,
                AU.username,
                AU.first_name, 
                AU.last_name
            FROM auth_user AU
            LEFT JOIN auth_user_groups AUG ON AUG.user_id = AU.id 
            ORDER BY AU.id ASC
        '''
        list_auth_group = SQL.sql_to_list(sql=sql, DB_name=DATA_BASE)
        map_auth = {}
        for row in list_auth_group:
            key = row["group_id"]
            if key not in map_auth:
                map_auth[key] = []
            map_auth[key].append(row)
        
        for res in result:
            key = res["id"]
            res['children'] = []
            if key in map_auth:
                res['children'] = map_auth[key]

        return JsonResponse(result=True, data=result)

    def set_group_edit_data(self, request, params):
        '''グループデータ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            id,
            name
        FROM
            auth_group
        WHERE 1 = 1
            {0}
        ORDER BY
            id
        '''

        if 'id' in params and params['id']:
            sql_condition.append(
                ' AND id = %(id)s'
            )
            sql_param['id'] = params['id']

        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_list(sql=sql, params=sql_param, DB_name=DATA_BASE)

        for res in result:
            sql_res = '''
            SELECT
                auth_user_groups.user_id,
                auth_user.username
            FROM auth_user_groups
            LEFT JOIN auth_user ON auth_user.id=auth_user_groups.user_id
            WHERE
                group_id = %(id)s
            '''

            result_res = SQL.sql_to_list(
                sql=sql_res, params={'id': res['id']}, DB_name=DATA_BASE)
            res['children'] = result_res

        sql_check = '''
            SELECT
                menu_path
            FROM auth_menu
            WHERE
                group_id = %(id)s
            '''

        result_auth_menu = SQL.sql_to_list(
            sql=sql_check, params={'id': params['id']}, DB_name=DATA_BASE)

        # menu list
        menu_list = []
        for row in result_auth_menu:
            menu_list.append(row["menu_path"])
        for new_result in result:
            new_result['menu_list'] = menu_list

        return JsonResponse(result=True, data=result)

    def get_user_list(self, request, params):
        '''ユーザーリスト取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            id,
            username
        FROM
            auth_user
        where username != 'guest'
        ORDER BY
            id
        '''

        result = SQL.sql_to_list(sql=sql, params=sql_param, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def get_edit_user_list(self, request, params):
        '''グループデータ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
          id as user_id,
		  username
		from auth_user
        where username != 'guest' and (id > 48 or id = 2)
        order by id
        '''

        result = SQL.sql_to_list(sql=sql, params={}, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def set_group_data(self, request, params):
        '''ユーザー保存取得'''
        auth_group = AuthGroup()

        auth_group.id = auth_group.next_value()
        group_id = auth_group.id
        auth_group.name = params['group_name']
        auth_group.save()

        if 'user_ids' in params and params['user_ids']:
            for user in params['user_ids']:
                auth_user_groups = AuthUserGroups()
                auth_user_groups.id = auth_user_groups.next_value()
                auth_user_groups.user_id = user
                auth_user_groups.group_id = group_id
                auth_user_groups.save()
        # menu
        menu_list = params["menu_list"]
        for menu in menu_list:
            auth_menu = AuthMenu()
            auth_menu.id = auth_menu.next_value()
            auth_menu.group_id = group_id
            auth_menu.menu_path = menu_list[menu]
            auth_menu.save()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def set_edit_group_data(self, request, params):
        '''ユーザーedit 保存取得'''
        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        AuthUserGroups.objects.filter(group_id=params['id']).delete()
        if 'user_ids' in params and params['user_ids']:
            for user in params['user_ids']:
                auth_user_groups = AuthUserGroups()
                auth_user_groups.id = auth_user_groups.next_value()
                auth_user_groups.user_id = user
                auth_user_groups.group_id = params['id']

                auth_user_groups.save()

        sql_check = '''
        SELECT
            id
        FROM 
            auth_menu
        WHERE 
            group_id = %(group_id)s
        '''

        result_check = SQL.sql_to_list(
            sql=sql_check, params={'group_id': params['id']}, DB_name=DATA_BASE)

        for new_check in result_check:
            auth_menu = AuthMenu.objects.using(
                DATA_BASE).get(pk=new_check['id'])
            auth_menu.delete()
        group_id = params['id']
        # menu
        menu_list = params["menu_list"]
        for menu in menu_list:
            auth_menu = AuthMenu()
            auth_menu.id = auth_menu.next_value()
            auth_menu.group_id = group_id
            auth_menu.menu_path = menu_list[menu]
            auth_menu.save()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def del_group_data(self, request, params):
        '''削除'''
        AuthGroup.objects.filter(id=params["id"]).delete()

        return JsonResponse(result=True)
