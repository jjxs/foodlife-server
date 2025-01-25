
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
                                       MstIngredientsCat, TakeoutUser, Seat)
from app.exception.web import WebException
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class TakeoutUserManagerApi(BaseAPI):

    def get_company_data(self, request, params):
        request = self.request
        DATA_BASE = 'ami'
        sql_condition = []
        sql_param = {}

        result = []
        sql = '''
        select takeout_user.*,seat.name as seat_name
        from
        takeout_user
        left join seat
        on seat.id = takeout_user.seat_no
        order by takeout_user.id
        '''
        result = SQL.sql_to_list(
            sql=sql, params={}, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def get_company_edit_data(self, request, params):
        '''坐席編集データ取得'''

        DATA_BASE = 'ami'

        result = []

        if 'id' in params and params['id']:
            sql = '''
            SELECT
            *
            FROM takeout_user
            WHERE
                id = %(id)s
            '''

            result = SQL.sql_to_list(
                sql=sql, params={'id': params['id']}, DB_name=DATA_BASE)

        data = {
            'result': result
        }

        return JsonResponse(result=True, data=data)

    def set_company_data(self, request, params):
        DATA_BASE = 'ami'
        # 会社信息更新
        takeout_user = TakeoutUser()
        seat = Seat()
        if 'id' in params and params['id']:
            takeout_user = TakeoutUser.objects.using(
                DATA_BASE).get(pk=params['id'])
            seat = Seat.objects.using(
                DATA_BASE).get(pk=params['seat_no'])
            seat.name = params['user_name']
            seat.save()
        else:
            # 新增会社默认添加坐席(编号-seat_no从100001开始,名字和公司名字一致)
            seat.id = seat.next_value()
            seat.seat_no = self.get_max_company()
            seat.name = params['user_name']
            seat.start = datetime.datetime.now()
            seat.usable = True
            seat.takeout_type = 1
            seat.save()
            params['id'] = takeout_user.next_value()
            params['create_time'] = datetime.datetime.now()
            params['seat_no'] = seat.id

        takeout_user.save(request=request, using=DATA_BASE, values=params)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_max_company(self):
        DATA_BASE = 'ami'
        number = 0
        sql = '''
        SELECT
            max(seat_no)
        FROM
            seat
        WHERE 
             takeout_type= 1
        '''
        seatgroup_list = SQL.sql_to_list(sql=sql, params={}, DB_name=DATA_BASE)
        if(len(seatgroup_list) > 0):
            number = int(seatgroup_list[0]['max'])+1
        if(number > 100001):
            return number
        else:
            return 100001

    def get_company_add_data(self, request, params):
        '''坐席編集データ取得'''

        data = {
            'seatgroup': self.get_seatgroup_list(),
            'typegroup': self.get_type_list('3'),
            'smokegroup': self.get_type_list('4'),
        }

        return JsonResponse(result=True, data=data)

    def delete_company_data(self, request, params):
        '''坐席データ削除'''

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                if len(params['rows']) > 0:
                    takeout_user = TakeoutUser.objects.using(
                        DATA_BASE).get(pk=params['rows']['id'])
                    takeout_user.delete()
                    seat = Seat.objects.using(
                        DATA_BASE).get(pk=params['rows']['seat_no'])
                    seat.delete()

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

