
import datetime


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
from app.db.models.mst import MstUser2


class UserApi(BaseAPI):

    def get_user_data(self, request, params):
        '''ユーザーデータ取得'''

        sql_param = {}
        sql_condition = []

        sql = '''
        SELECT
            id,
            account,
            user_name,
            CASE WHEN sex = 0 THEN '男' ELSE '女' END AS sex,
			CASE WHEN level = 1 THEN 'VIP1' WHEN level = 2 THEN 'VIP2' ELSE 'VIP3' END AS level,
            phone_number
        FROM mst_user
        WHERE 1 = 1
            {0}
        ORDER BY id
        '''
        if 'keyword' in params and params['keyword']:
            sql_condition.append(
                ' AND (user_name LIKE %(keyword)s)'
            )
            sql_param['keyword'] = '%' + params['keyword'] + '%'

        # result = SQL.sql_to_list(sql=sql, params=sql_param, DB_name=DATA_BASE)
        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_list(sql=sql, params=sql_param)

        return JsonResponse(result=True, data=result)

    def get_user_edit_data(self, request, params):
        '''ユーザー編集データ取得'''

        result = []

        if 'id' in params and params['id']:
            sql = '''
            SELECT
                id,
                account,
                level,
                point,
                gift_count,
                user_name,
                sex,
                phone_number,
                remarks
            FROM mst_user
            WHERE
                id = %(id)s
            '''

            result = SQL.sql_to_list(
                sql=sql, params={'id': params['id']})

        return JsonResponse(result=True, data=result)

    def set_user_data(self, request, params):
        '''ユーザーデータ保存'''

        user = MstUser2()

        user.account = params['account']
        user.password = params['password']
        user.level = params['level']
        user.point = 0
        user.gift_count = 0
        user.user_name = params['user_name']
        user.sex = params['sex']
        user.phone_number = params['phone_number']
        user.remarks = params['remarks']
        user.save()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def set_edit_user_data(self, request, params):
        '''ユーザーデータ編集'''

        user = MstUser2.objects.get(pk=params['id'])

        user.account = params['account']
        user.password = params['password']
        user.level = params['level']
        user.user_name = params['user_name']
        user.sex = params['sex']
        user.phone_number = params['phone_number']
        user.remarks = params['remarks']
        user.save()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def delete_user(self, request, params):
        '''ユーザーデータ削除'''

        user = MstUser2.objects.get(pk=int(params['id']))
        user.delete()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))