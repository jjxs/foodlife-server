from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import authentication, permissions, serializers

from django.forms.models import model_to_dict
from master.models.guest import Guest, GuestUser
from master.models.menu import *
from master.models.seat import SeatStatus, SeatFree
from master.models.order import *
from master.models.master import *
import master.data.cache_data as cache_data
from master.data.util_tax import UtilTax
from master.serializer.order import OrderSerializer, OrderDetailSerializer

from common.util import Util
import common.sql as Sql
from common.log import logger
from common.web.json import JsonResult
from common.views.view import SampleAPIView
from common.permission.controller import UserRoleAuthenticated
from common import const
import json
import sys
import channels.layers
from asgiref.sync import async_to_sync
import datetime

from master.data.const import SpecialMenu
import common.saas as saas


class OrderListController(SampleAPIView):

    def get_order(self, request, *args, **kwargs):

        params = {}
        sql_where = ''

        # 席指定
        if 'seat_id' in request.GET:
            seat_id = request.GET['seat_id']
            params['seat_id'] = seat_id
            sql_where += ' and ord.seat_id = %(seat_id)s'

        # 利用中のみ取得
        if not 'get_all' in request.GET:
            sql_where += ' and seat_status.id is not null '

        
        if 'desc' in request.GET:
            sql_where += ' ORDER BY ord.id DESC'

        sql = Sql.get('get_order')
        sql = sql.format(sql_where)
        rows = Sql.sql_to_dict(sql, params)
        return Response(rows)

    def get_order_detail(self, request, *args, **kwargs):

        params = {}
        sql_where = ''

        # 席指定
        if 'seat_id' in request.GET:
            seat_id = request.GET['seat_id']
            params['seat_id'] = seat_id
            sql_where += ' and ord.seat_id = %(seat_id)s'

        # 利用中のみ取得
        if not 'get_all' in request.GET:
            sql_where += ' and seat_status.id is not null '

        if 'desc' in request.GET:
            sql_where += ' ORDER BY detail.id DESC'

        sql = Sql.get('get_order_detail')
        sql = sql.format(sql_where)
        rows = Sql.sql_to_dict(sql, params)
        print(sql)
        return Response(rows)


class OrderHistoryController(SampleAPIView):
    '''
        現在の注文履歴を取得処理、席指定が必須
    '''

    # 認証
    permission_classes = (UserRoleAuthenticated,)

    def get_order(self, request, *args, **kwargs):

        params = {
            'seat_id': request.GET['seat_id']
        }

        sql = Sql.get('get_order')
        sql_where = ' and ord.seat_id = %(seat_id)s and seat_status.id is not null '
        sql = sql.format(sql_where)
        rows = Sql.sql_to_dict(sql, params)
        return Response(rows)


class OrderController(SampleAPIView):

    # 認証
    permission_classes = (UserRoleAuthenticated,)

    # def send_result(self, seat_id):
    #     # json_data = json.loads(text_data)
    #     # data = json_data['data']
    #     print("###########  OrderController send_result################")
    #     channel_layer = channels.layers.get_channel_layer()
    #     channel_layer.group_send(
    #         '__OrderConfirmConsumer__',
    #         {
    #             'type': 'send_message',
    #             'result': "ok"
    #         })

    def confirm(self, request, *args, **kwargs):
        '''
            放題注文の確認処理
        '''

        detail_free_id = request.data["detail_free_id"]

        # 事务处理開始
        with transaction.atomic():

            # 注文明細取得
            detail_menu_free = OrderDetailMenuFree.objects.get(id=detail_free_id)

            menu_free = detail_menu_free.menu_free
            time = menu_free.usable_time

            now = Util.current()
            end = now + datetime.timedelta(minutes=time)

            detail_menu_free.usable = True
            detail_menu_free.start = now
            detail_menu_free.end = end
            detail_menu_free.save()

        try:

            # 放題メニューリストを取得
            detail = detail_menu_free.order_detail
            menu_details = MenuFreeDetail.objects.filter(menu_free__menu__id=detail.menu.id)
            freemenu_list = [detail.menu.id for detail in menu_details]

            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                saas.group_name(saas.id(request), '__SeatConsumer__' + str(detail.order.seat.id)),
                {
                    'type': 'freemenu_order_confirm',
                    'result': True,
                    'freemenu_list': freemenu_list
                })
        except:
            logger.error("Unexpected error: {0}".format(sys.exc_info()[0]))

        # クライアント側更新用明細情報を取得
        sql_where = ' and detail.id = %(detail_id)s '
        sql_where += ' and ord.seat_id = %(seat_id)s '
        sql_where += ' and seat_status.id is not null '
        sql = Sql.get('get_order_detail')
        sql = sql.format(sql_where)
        params = {
            'detail_id': detail.id,
            'seat_id': detail.order.seat.id
        }
        rows = Sql.sql_to_dict(sql, params)

        return Response(JsonResult(result=True, message="確認は完了しました。", data=rows))

    # def order_menufree(self, request, *args, **kwargs):
    #     """
    #     放題注文処理（放題注文画面からの注文）
    #     """

    #     menu_id = request.data["menu_id"]
    #     menu_free_id = request.data["menu_free_id"]
    #     count = request.data["count"]
    #     key = request.data["key"]
    #     seat_status = SeatStatus.objects.get(security_key=key)

    #     # 現在テーブル利用不可の場合、注文できません
    #     if seat_status is None:
    #         result = JsonResult(message="テーブルが利用できません！")
    #         return Response(result)

    #     # 事务处理開始
    #     with transaction.atomic():

    #         # 注文テーブルへ登録
    #         order = Order.objects.create(
    #             order_no=Util.current_string("%Y%m%d%H%M%S%f"),
    #             counter_no=seat_status.counter_no,
    #             seat=seat_status.seat,
    #             user=request.user
    #         )

    #         menu = Menu.objects.get(id=menu_id)

    #         menu_free = MenuFree.objects.get(id=menu_free_id)
    #         # 注文明細作成
    #         detail = OrderDetail.objects.create(
    #             order=order,
    #             menu=menu,
    #             count=count,
    #             cancelable=True,
    #             price=menu.price,
    #             ori_price=menu.ori_price
    #         )

    #         # 放題の注文明細作成
    #         OrderDetailMenuFree.objects.create(
    #             order=order,
    #             order_detail=detail,
    #             menu_free=menu_free,
    #             usable=False)

    #     # 注文画面リフレッシュ通知
    #     try:
    #         channel_layer = channels.layers.get_channel_layer()
    #         async_to_sync(channel_layer.group_send)(
    #             '__OrderConsumer__',
    #             {
    #                 'type': 'send_message',
    #                 'data': {
    #                     "type": "refresh"
    #                 }
    #             })
    #     except:
    #         print(sys.exc_info()[0])

    #     return Response(JsonResult(result=True, message="注文は完了しました。"))

    def order(self, request, *args, **kwargs):
        """ 一般注文処理 """
        orders = request.data["orders"]
        key = request.data["key"]
        ship_addr = ship_name = ship_tel = ship_time = ''
        if "ship_info" in request.data:
            ship_info = request.data['ship_info']
            if 'ship_addr' in ship_info:
                ship_addr = ship_info['ship_addr']
            if 'ship_name' in ship_info:
                ship_name = ship_info['ship_name']
            if 'ship_tel' in ship_info:
                ship_tel = ship_info['ship_tel']
            if 'ship_time' in ship_info:
                ship_time = ship_info['ship_time']

        seat_status = SeatStatus.objects.get(security_key=key)


        # 現在テーブル利用不可の場合、注文できません
        if seat_status is None:
            result = JsonResult(message="テーブルが利用できません！")
            return Response(result)

        # Kitchen連絡用データ
        kitchen_data = {}
        
        start_menu_free = False
        if 'start_menu_free' in request.data:
            start_menu_free = request.data['start_menu_free']

        # 事务处理開始
        with transaction.atomic():

            # 注文テーブルへ登録
            order = Order.objects.create(
                order_no=Util.current_string("%Y%m%d%H%M%S%f"),
                counter_no=seat_status.counter_no,
                seat=seat_status.seat,
                user=request.user,
                ship_addr=ship_addr,
                ship_name=ship_name,
                ship_tel=ship_tel,
                ship_time=ship_time
            )

            free_menu_ids = self.getMenuFreeMenuId(order.seat_id)
            # course_menu = self.getCourseMenu()

            # 注文明細テーブルへ登録
            for value in orders:
                key = value['menu']['id']
                menu = Menu.objects.get(id=key)

                
                if start_menu_free:
                    SeatFree.objects.create(
                        seat=seat_status.seat,
                        menu_free_id = menu.id,
                        start=Util.current(),
                        status=1
                    )
                price = menu.price
                #　食べ放題判断, チェック注文時間含めてチェックを行います。
                # if ('free' in value) and value['free']:
                if len(free_menu_ids) and menu.id in free_menu_ids:
                    price = 0
                else:
                    price = self.get_price(price, value['menu'])
                # if len(rows) == 0:
                #     # 食べ放題できないと判断し場合、エラーで返す。
                #     return Response(JsonResult(result=False, message="食べ放題の注文はご利用できませんので、ご確認してください。"))

                # 通常, CODE:100 受付でステータス
                status_master = cache_data.get_master_by_code(const.MasterGroup.order_detail_status, const.OrderDetailStatus.Code_100)
                detail_option = {}
                if 'course' in value['menu']:
                    course = value['menu']['course']
                    for i, course_menu_item in enumerate(course):
                        if course_menu_item['selected']:
                            detail_option[course_menu_item['id']] =  {
                                'id'   : course_menu_item['id'],
                                'name' : course_menu_item['name'],
                                'index': i if value['menu']['level'] == 1 else course_menu_item['group_id'],
                                'status': 0
                            }
                # 注文明細作成
                detail = OrderDetail.objects.create(
                    order=order,
                    menu=menu,
                    count=value["count"],
                    cancelable=True,
                    option=detail_option,
                    price=price,
                    ori_price=menu.ori_price,
                    menu_option=value["menu"]["menu_options"]
                )

                # 注文明細ステータス作成
                detail_status = OrderDetailStatus.objects.create(
                    order_detail=detail,
                    status=status_master,
                    user=request.user,
                    current=True)

                #　受付データを整理 =>キチン監視へ送信用
                if status_master.code == const.OrderDetailStatus.Code_100:
                    # print("#####################################")
                    # print(order.order_time)
                    # # メニュー所属マスタID（管理用分類）を取得
                    # print(menu)
                    master_id = cache_data.get_master_by_menu(menu.id)
                    data = {
                        'order_id': order.id,
                        'order_time': order.order_time,
                        'detail_id': detail.id,
                        'count': detail.count,
                        'price': int(detail.price),
                        'menu_id': menu.id,
                        'menu_no': menu.no,
                        'menu_name': menu.name,
                        'menu_note': menu.note,
                        'menu_option': detail.menu_option,
                        'seat_id': seat_status.seat.id,
                        'seat_no': seat_status.seat.seat_no,
                        'seat_name': seat_status.seat.name,
                        'detail_status_id': detail_status.id,
                        'status_code': status_master.code,
                        'status_username': request.user.username,
                        'option':detail_option,
                        'menu_image': menu.image,
                        'ship_addr': order.ship_addr,
                        'ship_name': order.ship_name,
                        'ship_tel': order.ship_tel,
                        'ship_time': order.ship_time
                    }
                    if master_id in kitchen_data:
                        kitchen_data[master_id].append(data)
                    else:
                        kitchen_data[master_id] = []
                        kitchen_data[master_id].append(data)

        # Kitchenへ通常
        for key, value in kitchen_data.items():
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                saas.group_name(saas.id(request), '__KitchenConsumer__'),
                {
                    'type': 'order_add',
                    'master_id': key,
                    'kitchen_data': Util.encode(kitchen_data[key])
                })
        if start_menu_free:
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                saas.group_name(saas.id(request), '__SeatConsumer__' + str(detail.order.seat.id)),
                {
                    'type': 'freemenu_order_confirm',
                    'result': True,
                    'freemenu_list': []
                })

        return Response(JsonResult(result=True, message="注文は完了しました。"))

    def order_other(self, request, *args, **kwargs):
        """ その他注文処理 """
        orders = request.data["orders"]
        key = request.data["key"]
        seat_status = SeatStatus.objects.get(security_key=key)

        # print( """ その他注文処理 """)
        # print(orders)
        # print(key)

        # 現在テーブル利用不可の場合、注文できません
        if seat_status is None:
            result = JsonResult(message="テーブルが利用できません！")
            return Response(result)

        # 事务处理開始
        with transaction.atomic():

            # 注文テーブルへ登録
            order = Order.objects.create(
                order_no=Util.current_string("%Y%m%d%H%M%S%f"),
                counter_no=seat_status.counter_no,
                seat=seat_status.seat,
                user=request.user
            )

            # 注文明細テーブルへ登録
            for item in orders:

                if item["model"] == '0':
                    # 税抜の場合
                    menu = Menu.objects.get(no=SpecialMenu.Other_tax_none)
                    price = item["price"]
                else:
                    # 税込の場合
                    menu = Menu.objects.get(no=SpecialMenu.Other_tax_in)
                    price = item["price"]

                # 通常, CODE:999 完成
                status_master = cache_data.get_master_by_code(const.MasterGroup.order_detail_status, const.OrderDetailStatus.Code_999)

                # 注文明細作成
                detail = OrderDetail.objects.create(
                    order=order,
                    menu=menu,
                    count=item["count"],
                    cancelable=True,
                    price=price,
                    ori_price=price
                )

                # 注文明細ステータス作成
                detail_status = OrderDetailStatus.objects.create(
                    order_detail=detail,
                    status=status_master,
                    user=request.user,
                    current=True)

        return Response(JsonResult(result=True, message="注文は完了しました。"))


    def getCourseMenu(self):
        sql = '''
            SELECT 
                menu.*,
                menu_course.id AS course_id,
                menu_course.menu_id AS course_menu_id
            FROM  menu_course 
            INNER JOIN menu_course_detail ON menu_course_detail.menu_course_id = menu_course.id
            INNER JOIN MENU ON menu.id = menu_course_detail.menu_id
            ORDER BY menu_course.id, menu_course_detail.id ASC
        '''
        menulist = Sql.sql_to_dict(sql)
        result = {}
        for item in menulist:
            id = item['course_menu_id']
            if id not in result:
                result[id] = []
            result[id].append(item)
        return result
    
    def getMenuFreeMenuId(self, seat_id):
        params = {
            'seat_id': seat_id
        }

        sql = '''
                SELECT mfd.menu_id FROM order_detail
                    INNER JOIN menu_free ON order_detail.menu_id=menu_free.menu_id
                    INNER JOIN menu_free_detail mfd ON mfd.menu_free_id=menu_free.id
                    INNER JOIN "order" ord ON order_detail.order_id=ord.id AND ord.seat_id=%(seat_id)s
                    INNER JOIN seat_free ON ord.seat_id=seat_free.seat_id AND seat_free.status=1
            '''
        result = Sql.sql_to_dict(sql, params)
        menu_free_id = []
        if len(result):
            for item in result:
                menu_free_id.append(
                        item['menu_id']
                    )
        return menu_free_id


    def get_price(self, price, menu):
        if 'menu_options' in menu:
            options = menu['menu_options']
            for k in options:
                if 'select_price' in options[k] and options[k]['select_price']:
                    add_price = options[k]['select_price']
                    price = price + int(add_price)

        return price

