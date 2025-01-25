from django.db import transaction
from django.db import connection
from rest_framework.response import Response
from common.util import Util
from common.log import logger
from common.web.json import JsonResult
from common.views.view import SampleAPIView
from common.permission.controller import UserRoleAuthenticated
from common import const
from master.models.order import *

import master.data.cache_data as cache_data
from common.exception.web import WebLogicException
import common.sql as Sql

import channels.layers
from asgiref.sync import async_to_sync
import common.saas as saas


class KitchenController(SampleAPIView):

    # 認証
    permission_classes = (UserRoleAuthenticated,)

    def get_task(self, request, *args, **kwargs):

        sql = Sql.get("get_kitchen_task")
        sql_params0 = r" "
        sql_params1 = r" "
        params = {}

        if "today" in request.data and request.data["today"]:
            sql_params0 += r" AND order_time >= now()::date "

        if "list" in request.data and request.data["list"]:
            sql_params1 += r" inner join menu_category category on category.menu_id = menu.id and category.category_id in  %(list)s "
            params["list"] = tuple(request.data["list"])

        sql = sql.format(sql_params0, sql_params1)

        rows = Sql.sql_to_dict(sql, params)

        # result = self.to_json()
        return Response(rows)

    def goto_next(self,  request, *args, **kwargs):

        detail_id = request.data["detail_id"]
        detail_status_id = request.data["detail_status_id"]
        current_status_code = request.data["current_status_code"]
        next_status_code = request.data["next_status_code"]

        menu_id = request.data["menu_id"]
        task = request.data["task"]
        # current_status_master = cache_data.get_master_by_code(const.MasterGroup.order_detail_status, current_status_code)

        # 事务处理開始
        with transaction.atomic():

            detail_status = OrderDetailStatus.objects.get(id=detail_status_id)

            if detail_status.status.code != current_status_code:
                return Response(JsonResult(result=True, message="該当テスクのステータスが変更しました、ご確認してください。"))

            # 変更先ステータスデータ
            next_status_master = cache_data.get_master_by_code(const.MasterGroup.order_detail_status, next_status_code)

            # 現在明細の更新
            detail = OrderDetail.objects.get(id=detail_id)
            detail.status = next_status_master
            detail.save()

            # 新ステータスの作成
            next_status = OrderDetailStatus.objects.create(
                order_detail=detail,
                status=next_status_master,
                user=request.user,
                current=True)

            # TODO: 遷移可能チェック
            # ...
            # 現在ステータスの更新,すべて更新、同時に更新ある場合、後勝ち
            Sql.execute('''
                update order_detail_status set current = false
                where order_detail_id = %(order_detail_id)s and id != %(id)s
            ''', {
                'order_detail_id': detail_status.order_detail.id,
                'id': next_status.id
            })
            # detail_status.current = False
            # detail_status.save()

            count = Sql.sql_to_one('''
                select count(id) from order_detail_status where order_detail_id = %(order_detail_id)s and current = true
            ''', {'order_detail_id': detail_status.order_detail.id})

            if count != 1:
                raise WebLogicException("該当テスクのステータスが変更しました、最新状況をご確認してください。")

            task['detail_status_id'] = next_status.id
            task['status_code'] = next_status_master.code
            task['status_username'] = request.user.username

        master_id = cache_data.get_master_by_menu(menu_id)
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            saas.group_name(saas.id(request), '__KitchenConsumer__'),
            {
                'type': 'order_add',
                'master_id': master_id,
                'kitchen_data': Util.encode([task]),
            })

        return Response(JsonResult(result=True, message="ステータスが変更しました。"))

    def remove_task(self,  request, *args, **kwargs):

        detail_id = request.data["detail_id"]
        order_id = request.data["order_id"]

        # 事务处理開始
        with transaction.atomic():

            Sql.execute("delete from order_detail_status where order_detail_id = %(detail_id)s ", {"detail_id": detail_id})
            Sql.execute("delete from order_detail where id = %(detail_id)s ", {"detail_id": detail_id})
            count = Sql.sql_to_one("select count(0) from order_detail where order_id = %(order_id)s ", {"order_id": order_id})

            if count == 0:
                Sql.execute('delete from "order" where id = %(order_id)s ', {"order_id": order_id})

        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            saas.group_name(saas.id(request), '__KitchenConsumer__'),
            {
                'type': 'order_delete',
                'detail_id': Util.encode([detail_id])
            })

        return Response(JsonResult(result=True, message="タスクが削除されました。"))

    
    def order_option(self,  request, *args, **kwargs):
        detail_id = request.data['detail_id']
        option_id = str(request.data['option_id'])
        status = 1
        if 'status' in request.data:
            status = request.data['status']
            
        with transaction.atomic():
            detail = OrderDetail.objects.get(id=detail_id)
            option = detail.option
            if option_id in option:
                option[option_id]['status'] = status
            detail.option = option
            detail.save()
        
            
            master_id = cache_data.get_master_by_menu(detail.menu_id)
            task = request.data["task"]
            # task['menu_option'] = detail.option
            task['option'] = detail.option
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                saas.group_name(saas.id(request), '__KitchenConsumer__'),
                {
                    'type': 'order_add',
                    'master_id': master_id,
                    'kitchen_data': Util.encode([task]),
                })
        return Response(JsonResult(result=True, message="ステータスが変更しました。"))