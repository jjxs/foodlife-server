
from datetime import datetime as dt
from zipfile import is_zipfile

from botocore import model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from master.models.seat import *
from master.models.counter import *
from master.models.order import *

import app.common.message as Message
import app.const as Const
import app.util as Util
from app.db.models.store_table import (AuthUser, MstIngredients,
                                       MstIngredientsCat, Seat)
from app.exception.web import WebException
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from django.contrib.auth import get_user_model
import common.sql as Sql


class CounterApi(BaseAPI):

    def lists(self, request, kwargs):

        params = {}
        sql_counter_details = r''' 
            SELECT counter_detail.*,
                (CASE WHEN date_part('hour',counter_detail.create_time)<8 THEN 1 ELSE 0 END) as lunch,
                master_data.code,
                master_data.display_name,
                auth_user.username, counter.delete as is_delete
            FROM counter_detail
            LEFT JOIN master_data ON counter_detail.pay_method_id = master_data.id
            LEFT JOIN counter ON counter.id = counter_detail.counter_id
            LEFT JOIN auth_user ON auth_user.id = counter_detail.user_id
            WHERE 1 = 1 
            AND counter_detail.canceled IS NOT TRUE
            {0} 
            ORDER BY counter_detail.create_time DESC
            '''

        sql_formart_counter_details = ""

        if request.data["begin"]:
            begin_format = self._format_date(request.data["begin"], '00:00:00')
            sql_formart_counter_details += f" AND counter.create_time >= '{begin_format}' "

        if request.data["end"]:
            end_format = self._format_date(request.data["end"], '23:59:59')
            sql_formart_counter_details += f" AND counter.create_time <= '{end_format}' "

        if request.data['paymethod']:
            paymethod = request.data['paymethod']
            sql_formart_counter_details += f"  AND counter_detail.pay_method_id = {paymethod} "

        if request.data['receipt_al'] is True and request.data['receipt_ns'] is not True:
            sql_formart_counter_details += f"  AND counter_detail.print_count > 0 "

        if request.data['receipt_ns'] is True and request.data['receipt_al'] is not True:
            sql_formart_counter_details += f"  AND counter_detail.print_count = 0 "

        if request.data['delete_al'] is True and request.data['delete_ns'] is not True:
            sql_formart_counter_details += f"  AND counter.delete IS TRUE "
            
        if request.data['delete_ns'] is True and request.data['delete_al'] is not True:
            sql_formart_counter_details += f"  AND counter.delete IS NOT TRUE "

        sql = sql_counter_details.format(sql_formart_counter_details)
        counter_details = Sql.sql_to_dict(sql, params)
        return JsonResponse(result=True, data=counter_details)

    def _format_date(self, date: str, point) -> str:
        date = dt.strptime(date, '%Y/%m/%d').date()
        return "{0}-{1}-{2} {3}".format(date.year, str(date.month).rjust(2, '0'), str(date.day).rjust(2, '0'), point)

    def delete(self, request, kwargs):
        counter_detail_id = kwargs["id"]
        # print(counter_detail_id)
        counterDetail = CounterDetail.objects.get(id=counter_detail_id)
        counter_no = counterDetail.no
        # print(counter_no)
        with transaction.atomic():
            counter_id = counterDetail.counter_id
            # print(counter_id)
            counterDetailOrders = None
            # CounterDetail delete
            CounterDetail.objects.filter(id=counter_detail_id).delete()
            order_detail_ids = []
            delete_all = False
            if not CounterDetail.objects.filter(counter_id=counter_id).exists():
                # Counter delete
                Counter.objects.filter(id=counter_id).delete()
                SeatStatusHistory.objects.filter(
                    counter_no=counter_no).delete()

                CounterSeat.objects.filter(counter_id=counter_id).delete()

                counterDetailOrders = CounterDetailOrder.objects.filter(
                    counter_id=counter_id).all()
                # print(counterDetailOrders)
                for item in counterDetailOrders:
                    order_detail_ids.append(item.order_detail_id)
                CounterDetailOrder.objects.filter(
                    counter_id=counter_id).delete()

                delete_all = True

            # CounterDetailOrder delete
            if len(order_detail_ids) == 0:
                counterDetailOrders = CounterDetailOrder.objects.filter(
                    counter_detail_id=counter_detail_id).all()
                # print(counterDetailOrders)

                for item in counterDetailOrders:
                    order_detail_ids.append(item.order_detail_id)
                # print(order_detail_ids)

                # CounterDetailOrder delete
                CounterDetailOrder.objects.filter(
                    counter_detail_id=counter_detail_id).delete()

            # OrderDetailHistory delete
            order_ids = []
            orderDetailHistorys = OrderDetailHistory.objects.filter(
                id__in=order_detail_ids).all()
            for item in orderDetailHistorys:
                order_ids.append(item.order_id)
                # print(order_ids)
            OrderDetailHistory.objects.filter(id__in=order_detail_ids).delete()

            # OrderDetailStatusHistory delete
            OrderDetailStatusHistory.objects.filter(
                order_detail_id__in=order_detail_ids).delete()

            # OrderDetailMenuFreeHistory delete
            OrderDetailMenuFreeHistory.objects.filter(
                order_detail_id__in=order_detail_ids).delete()

            # OrderHistory delete
            if delete_all:
                OrderHistory.objects.filter(id__in=order_ids).delete()

        return JsonResponse(result=False, data=[], message="完了しました。")
