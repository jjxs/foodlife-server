from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import authentication, permissions, serializers
from common.log import logger
from common.web.json import JsonResult

from master.models.guest import Guest, GuestUser
from master.models.seat import Seat, SeatStatus
from master.models.order import Order
from restaurant.models.seat import SeatList, SeatCondition
from restaurant.serializer.seat import SeatListSerializer, SeatConditionSerializer
from master.serializer.seat import SeatSerializer, SeatStatusSerializer
from common.permission.controller import UserRoleAuthenticated
import common.sql as Sql
from common.util import Util
import uuid
from django.db import transaction
import channels.layers
from asgiref.sync import async_to_sync
import common.saas as saas
import sys
from master.data.const import SpecialMenu
from master.models.menu import Menu
from common.views.view import SampleAPIView
from common.permission.controller import UserRoleAuthenticated
import pytz
from datetime import datetime

# class SeatController(object):

#     @api_view(['POST'])
#     @permission_classes([UserRoleAuthenticated])
#     def start(request):
#         print(request.data)
#         serializer = SeatSerializer(data=request.data)
#         data = serializer.data if serializer.is_valid() else []
#         result = JsonResult(data)
#         return Response(result)


class SeatController(SampleAPIView):

    def get_seat_info(self, request, *args, **kwargs):

        seat_id = request.GET["seat_id"]
        seat = Seat.objects.get(pk=seat_id)
        status = SeatStatus.objects.get(seat=seat)
        menus = Menu.objects.filter(no=SpecialMenu.Table_charge)
        menu = menus[0]

        sql = '''
            SELECT SUM(COUNT) AS total
            FROM order_detail detail
            INNER JOIN menu ON menu.id = detail.menu_id
            LEFT JOIN "order" ord ON ord.id = detail.order_id
            INNER JOIN seat_status
                    ON seat_status.seat_id = ord.seat_id
                    AND seat_status.counter_no = ord.counter_no
            WHERE menu.no = %(menu_no)s
            AND   ord.seat_id = %(seat_id)s
        '''
        orders = Sql.sql_to_one(sql, {"menu_no": SpecialMenu.Table_charge, "seat_id": seat_id})

        data = {
            "current_number": 0 if not status.number else status.number,
            "current_orders": orders,
            "key": status.security_key,
            "menu_id": menu.id,
            "utype": status.utype
        }
        result = JsonResult(result=True, data=data)
        return Response(result)

    def update_number(self, request, *args, **kwargs):

        seat_id = request.data["seat_id"]
        number = request.data["number"]
        key = request.data["key"]
        utype = request.data["utype"]

        seat = Seat.objects.get(pk=seat_id)
        status = SeatStatus.objects.get(seat=seat)
        # 現在テーブル利用不可の場合、注文できません
        if status is None or status.security_key != key:
            result = JsonResult(message="テーブルが利用できません！")
            return Response(result)

        status.number = number
        status.utype = utype
        status.save()

        result = JsonResult(result=True, message="来客調整しました！")
        return Response(result)

    def free_status(self, request, *args, **kwargs):
        sql = "SELECT * FROM seat_free"
        result = JsonResult(data=Sql.sql_to_dict(sql), message='ok')
        return Response(result)

    def free_stop(self, request, *args, **kwargs):
        seat_id = request.data["seat_id"]
        sql = "delete from seat_free WHERE seat_id=%(seat_id)s"
        with transaction.atomic():
            Sql.execute(sql, { 'seat_id':seat_id } )

            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                saas.group_name(saas.id(request), '__SeatConsumer__' + str(seat_id)),
                {
                    'type': 'freemenu_order_confirm',
                    'result': True,
                    'freemenu_list': []
                })

        result = JsonResult(result=True, message="処理しました！")
        return Response(result)

    def change_seat(self, request, *args, **kwargs):
        result = {
            'message': '失敗しました。',
            'result':  False
        }

        params = {
            'target_seatid' : request.data["target_seatid"],
            'current_seatid': request.data["current_seatid"]
        }
            # 事务处理
        with transaction.atomic():
            # 放題」データ変更
            sql = "UPDATE seat_free SET seat_id=%(target_seatid)s WHERE seat_id=%(current_seatid)s"
            Sql.execute( sql, params )

            # 注文」データ変更
            sql = "UPDATE \"order\" SET seat_id=%(target_seatid)s WHERE seat_id=%(current_seatid)s"
            Sql.execute( sql, params )

            # 席利用者」データ変更
            data = Sql.sql_to_dict("SELECT * FROM seat_status WHERE seat_id=%(current_seatid)s", {'current_seatid':params['current_seatid']})
            sql = "UPDATE seat_status SET \"number\"=%(number)s, counter_no=%(counter_no)s , utype=%(utype)s WHERE seat_id=%(target_seatid)s "
            Sql.execute(sql, { 'number': data[0]['number'], 'counter_no': data[0]['counter_no'], 'utype': data[0]['utype'], 'target_seatid': params['target_seatid']})

        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            saas.group_name(saas.id(request), '__KitchenConsumer__'),
            {
                'type': 'order_change',
                'master_id': '',
                'kitchen_data': ''
            })
        result = {
            'message': '成功した',
            'result':  True
        }

        return Response(result)


    def stopall(self, request, *args, **kwargs):
        # 事务处理
        with transaction.atomic():
            seat_list = Seat.objects.all()
            for seat in seat_list:
                # TODO: ODER情報存在する場合、中止できない＝＞会計画面で終了する
                if Order.objects.filter(seat=seat).first():
                    result = JsonResult(result=False, message="注文情報存在しているため、営業終了できません、ご確認してください。")
                    return Response(result)

                try:
                    seat_status = SeatStatus.objects.get(seat=seat)

                    # 利用中止時間設定
                    # seat_status.end = Util.current()
                    tz = pytz.timezone('Asia/Tokyo')
                    seat_status.end = datetime.now(tz)
                    seat_status.save()

                    # テーブル利用状況から削除
                    seat_status.delete()
                except SeatStatus.DoesNotExist:
                    pass

                try:
                    group_name = "__SeatConsumer__{0}".format(seat.id)
                    channel_layer = channels.layers.get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        saas.group_name(saas.id(request), group_name),
                        {
                            'type': 'seat_using_stop'
                        })
                except:
                    logger.error(sys.exc_info()[0])

        result = JsonResult(result=True)
        return Response(result)


class SeatStatusController(APIView):

    # 認証
    permission_classes = (UserRoleAuthenticated,)


    def delete(self, request, format=None):
        '''
        テーブル利用中止
        '''

        # get　と　deleteはrequest body 使えない
        id = request.query_params.get("id")
        seat = Seat.objects.get(pk=id)

        try:
            seat_status = SeatStatus.objects.get(seat=seat)
        except SeatStatus.DoesNotExist:
            result = JsonResult(result=False, message="テーブル利用していない、ご確認してください。")
            return Response(result)

        # チェック注文状況、注文ある場合、中心できない

        # TODO: ODER情報存在する場合、中止できない＝＞会計画面で終了する
        if Order.objects.filter(seat=seat).first():
            result = JsonResult(result=False, message="注文情報存在しているため、中止できません、ご確認してください。")
            return Response(result)

            # 事务处理
        with transaction.atomic():

            # 利用中止時間設定
            # seat_status.end = Util.current()
            tz = pytz.timezone('Asia/Tokyo')
            seat_status.end = datetime.now(tz)
            seat_status.save()

            # # 利用履歴登録
            # SeatHistory.objects.create(
            #     Seat=seat,
            #     tablename="SeatStatus",
            #     history=Util.model_to_json(seat_status),
            #     user=request.user
            # )
            # テーブル利用状況から削除
            seat_status.delete()

        try:
            group_name = "__SeatConsumer__{0}".format(seat.id)
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                saas.group_name(saas.id(request), group_name),
                {
                    'type': 'seat_using_stop'
                })
        except:
            logger.error(sys.exc_info()[0])

        result = JsonResult(message="テーブル{0}({1})が利用可能になりました！".format(seat.name, seat.seat_no))

        return Response(result)

    def post(self, request, format=None):
        '''
        利用開始
        '''

        #  request body からデータを取る
        id = request.data.get("id")
        seat = Seat.objects.get(pk=id)

        seat_status, created = SeatStatus.objects.get_or_create(seat=seat)

        if not created:
            result = JsonResult(result=False, message="テーブル既に利用中になり、ご確認してください。")
            return Response(result)

        seat_status.counter_no = "{0}_{1}".format(seat.seat_no, Util.current_string("%Y%m%d%H%M%S%f"))
        # seat_status.start = Util.current()
        tz = pytz.timezone('Asia/Tokyo')
        seat_status.start = datetime.now(tz)
        seat_status.security_key = str(uuid.uuid4())

        seat_status.save()
        message = "テーブル{0}({1})が利用開始しました！".format(seat.name, seat.seat_no)
        try:
            group_name = "__SeatConsumer__{0}".format(seat.id)
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                saas.group_name(saas.id(request), group_name),
                {
                    'type': 'seat_using_start'
                })
        except:
            logger.error(sys.exc_info()[0])

        result = JsonResult(message=message)
        return Response(result)


class SeatListController(APIView):

    # 認証
    permission_classes = (UserRoleAuthenticated,)

    def get(self, request, format=None):

        seat_list = SeatList.objects.raw(Sql.get("find_seat_list"))
        data = SeatListSerializer(seat_list, many=True)
        result = JsonResult(data.data)

        return Response(result)

    #
    def post(self, request, format=None):

        serializer = SeatConditionSerializer(data=request.data)

        if not serializer.is_valid():
            result = JsonResult(result=False, message="検索条件が不正")
            return Response(result)

        condition = serializer.create()

        params = {
            "seat_type": tuple([-1]) if not condition.seat_type else tuple(condition.seat_type),
            "seat_type_str": True if not condition.seat_type else False,
            "seat_smoke_type": tuple([-1]) if not condition.seat_smoke_type else tuple(condition.seat_smoke_type),
            "seat_smoke_type_str": True if not condition.seat_smoke_type else False,
            "seat_group": tuple([-1]) if not condition.seat_group else tuple(condition.seat_group),
            "seat_group_str": True if not condition.seat_group else False
        }
        sql = Sql.get("find_seat_list")

        con = ""
        if condition.seat_number:
            con = " AND ( false "
            index = 0
            for item in condition.seat_number:
                nums = item.split("-")
                if len(nums) == 1:
                    con += " OR ( seat.number >= " + "%(min{0})s".format(index) + ")"
                    params["min{0}".format(index)] = int(nums[0])
                if len(nums) == 2:
                    con += " OR ( seat.number >= " + "%(min{0})s".format(index) + " AND seat.number <= " + "%(max{0})s".format(index) + ")"
                    params["min{0}".format(index)] = int(nums[0])
                    params["max{0}".format(index)] = int(nums[1])

                index += 1

            con += ")"

        con_usable = ""
        if condition.seat_usable == "1":
            con_usable = " AND seat_status.seat_id is null"

        if condition.seat_usable == "2":
            con_usable = " AND seat_status.seat_id is not null"

        if not condition.takeout_type:
            params['takeout_type'] = 0
            con += " AND (seat.takeout_type=0 or seat.takeout_type is null) "

        sql = sql.format(con, con_usable)
        print(sql, params)
        seat_list = SeatList.objects.raw(sql, params)
        data = SeatListSerializer(seat_list, many=True)
        result = JsonResult(data.data)

        return Response(result)
