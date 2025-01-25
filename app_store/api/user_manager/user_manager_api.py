
import datetime
from zipfile import is_zipfile

from botocore import model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
import app.util as Util
from app.db.models.store_table import (AuthUser, MstIngredients,
                                       MstIngredientsCat,Seat)
from app.exception.web import WebException
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserManagerApi(BaseAPI):

    def get_user_data(self, request, params):
        '''ユーザーデータ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            id,
            username,
            first_name,
            last_name,
			is_active,
            is_staff,
			is_superuser
        FROM auth_user
        WHERE username != 'guest' and (id > 48 or id = 2)
            {0}
        ORDER BY id
        '''
        if 'keyword' in params and params['keyword']:
            sql_condition.append(
                ' AND (username LIKE %(keyword)s)'
            )
            sql_param['keyword'] = '%' + params['keyword'] + '%'

        # result = SQL.sql_to_list(sql=sql, params=sql_param, DB_name=DATA_BASE)
        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_list(
            sql=sql, params=sql_param, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def get_user_edit_data(self, request, params):
        '''ユーザー編集データ取得'''

        DATA_BASE = 'ami'

        result = []

        if 'id' in params and params['id']:
            sql = '''
            SELECT
                id,
                username,
                first_name,
                last_name,
                is_active,
                is_staff,
                is_superuser
            FROM auth_user
            WHERE
                id = %(id)s
            '''

            result = SQL.sql_to_list(
                sql=sql, params={'id': params['id']}, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def set_user_data(self, request, params):
        '''ユーザーデータ保存'''

        DATA_BASE = 'ami'

        user = UserModel()
        auth_user = AuthUser()

        if'password' in params and params['password']:
            user.set_password(params['password'])
            auth_user.password = user.password

        if not params["last_name"]:
            params["last_name"] = " "

        auth_user.username = params['username']
        auth_user.first_name = params['first_name']
        auth_user.last_name = params['last_name']
        auth_user.is_superuser = params['is_superuser']
        auth_user.is_staff = params['is_staff']
        auth_user.is_active = params['is_active']
        auth_user.date_joined = datetime.datetime.now()

        auth_user.save()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def set_edit_user_data(self, request, params):
        '''材料データ保存'''

        DATA_BASE = 'ami'

        user = UserModel()
        auth_user = AuthUser.objects.using(
            DATA_BASE).get(pk=params['id'])
        # auth_user = AuthUser()

        if'password' in params and params['password']:
            user.set_password(params['password'])
            auth_user.password = user.password
            params['password'] = user.password
        else:
            params['password'] = auth_user.password

        auth_user.username = params['username']
        auth_user.is_active = bool(params['is_active'])
        auth_user.is_staff = bool(params['is_staff'])
        auth_user.is_superuser = bool(params['is_superuser'])
        if not params["last_name"]:
            params["last_name"] = " "

        auth_user.save(request=request, using=DATA_BASE, values=params)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def delete_cat_data(self, request, params):
        '''ユーザーデータ削除'''

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                for row in params['rows']:
                    cat = AuthUser.objects.using(
                        DATA_BASE).get(pk=row['id'])
                    cat.delete()

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))