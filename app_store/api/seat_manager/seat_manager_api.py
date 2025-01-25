
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

class SeatManagerApi(BaseAPI):

    def get_seat_data(self, request, params):
        request = self.request
        DATA_BASE = 'ami'
        sql_condition = []
        sql_param = {}

        result = []
        sql = '''
        SELECT seat.*
        ,master1.display_name as seat_type
        , master2.display_name as seat_smoke_type
        , seat_group.no as group_no
        , seat_group.name as group_name
        , case when seat_status.number is null then 0 else seat_status.number end as guest_number
        , seat_status.start as use_start
        FROM seat
        left join seat_group on seat_group.id = seat.group_id
        left join master_data master1 on master1.id = seat_type_id
        left join master_data master2 on master2.id = seat_smoke_type_id
        left join seat_status on seat_status.seat_id = seat.id
        WHERE seat.usable = true
        {0}
        ORDER BY group_no, seat_no
        '''

        if 'takeout' in params and params['takeout']==0:
            sql_condition.append(' and seat.takeout_type = 0')
        else:
            sql_condition.append(' and seat.takeout_type = 1')

        sql = sql.format('\n'.join(sql_condition))
        
        result = SQL.sql_to_list(
            sql=sql, params={}, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def get_seat_edit_data(self, request, params):
        '''坐席編集データ取得'''

        DATA_BASE = 'ami'

        result = []

        if 'id' in params and params['id']:
            sql = '''
            SELECT
            *
            FROM seat
            WHERE
                id = %(id)s
            '''

            result = SQL.sql_to_list(
                sql=sql, params={'id': params['id']}, DB_name=DATA_BASE)

        data = {
            'result': result,
            'seatgroup': self.get_seatgroup_list(),
            'typegroup': self.get_type_list('3'),
            'smokegroup': self.get_type_list('4'),
        }

        return JsonResponse(result=True, data=data)

    def get_seatgroup_list(self):
        '''カテゴリーリスト取得'''

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            id,
            no,
            name
        FROM
            seat_group
        ORDER BY
            id
        '''
        seatgroup_list = SQL.sql_to_list(sql=sql, params={}, DB_name=DATA_BASE)
        return seatgroup_list

    def get_type_list(self, params):
        '''カテゴリーリスト取得'''

        DATA_BASE = 'ami'
        sql_param = {}
        sql_condition = []
        sql = '''
        SELECT
            id,
            code,
            display_name as name
        FROM
            master_data
        where 1 = 1
           {0}
        ORDER BY
            id
        '''

        if params != '':
            sql_condition.append(
                ' AND (group_id = %(params)s)'
            )
            sql_param['params'] = params
            sql = sql.format('\n'.join(sql_condition))

        type_list = SQL.sql_to_list(
            sql=sql, params=sql_param, DB_name=DATA_BASE)
        return type_list

    def set_seat_data(self, request, params):
        DATA_BASE = 'ami'

        seat = Seat()
        if 'id' in params and params['id']:
            seat = Seat.objects.using(
                DATA_BASE).get(pk=params['id'])
        else:
            seat.id = seat.next_value()
            seat.start = datetime.datetime.now()
            seat.usable = True

        seat.seat_no = params['seat_no']
        seat.name = params['name']
        # seat.group_id = params['group_id']
        seat.seat_type_id = params['seat_type_id']
        seat.seat_smoke_type_id = params['seat_smoke_type_id']
        seat.number = params['number']
        seat.takeout_type = 0

        seat.save(request=request, using=DATA_BASE, values=params)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_seat_add_data(self, request, params):
        '''坐席編集データ取得'''

        data = {
            'seatgroup': self.get_seatgroup_list(),
            'typegroup': self.get_type_list('3'),
            'smokegroup': self.get_type_list('4'),
        }

        return JsonResponse(result=True, data=data)

    def delete_seat_data(self, request, params):
        '''坐席データ削除'''

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                if len(params['rows']) > 0:
                    seat = Seat.objects.using(
                        DATA_BASE).get(pk=params['rows']['id'])
                    seat.delete()

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))