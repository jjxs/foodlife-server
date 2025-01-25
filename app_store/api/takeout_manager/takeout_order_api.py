
import datetime
from os.path import join
from zipfile import is_zipfile

from botocore import model
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import authentication, permissions, serializers
from rest_framework_jwt.settings import api_settings

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
import app.util as Util
from app.db.models.store_table import Takeout, TakeoutOrder
from app.exception.web import WebException
from app.http.api import BaseAPI
from app.http.response import JsonResponse

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class TakeoutOrderApi(BaseAPI):

    def get_takeout_history(self, request, params):
        '''管理界面订单查询'''
        sql_param = {}
        sql_condition = []
        DATA_BASE = 'ami'

        sql = '''
            SELECT
                takeout_order.*,
                takeout_user.seat_no
            FROM
                takeout_order LEFT JOIN takeout_user ON takeout_order.user_id = takeout_user.id
            where 1 = 1
            {0}
            ORDER BY create_time DESC
        '''

        if 'keywordaddress' in params and params['keywordaddress']:
            sql_condition.append(
                ' AND (ship_addr LIKE %(keywordaddress)s)'
            )
            sql_param['keywordaddress'] = '%' + params['keywordaddress'] + '%'

        if 'keyworduser' in params and params['keyworduser']:
            sql_condition.append(
                ' AND (ship_name LIKE %(keyworduser)s)'
            )
            sql_param['keyworduser'] = '%' + params['keyworduser'] + '%'


        sql = sql.format('\n'.join(sql_condition))
        orders = SQL.sql_to_list(sql=sql, params=sql_param, DB_name=DATA_BASE)
        if(len(orders) == 0):
            result = []
            return JsonResponse(result=True, data=result)

        order_ids = []
        map_orders = {}
        for item in orders:
            # 拿订单号去查询相应菜品
            order_ids.append(item['id'])
            map_orders[item['id']] = item

        sql = '''
            SELECT
                *
            FROM
            takeout_order_detail
            where order_id in %(order_id)s
        '''
        details = SQL.sql_to_list(sql, {'order_id': order_ids})
        for item in details:
            order_id = item['order_id']
            if 'details' not in map_orders[order_id]:
                map_orders[order_id]['details'] = []

            map_orders[order_id]['details'].append(item)

        result = map_orders.values()
        return JsonResponse(result=True, data=result)
    
    def order(self, request, params):
        id = params['id']
        order = TakeoutOrder.objects.get(id=id)
        order.order_status = 1
        order.save()
        return JsonResponse(result=True, data=order.__dict__)

