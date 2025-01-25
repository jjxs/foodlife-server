from datetime import datetime
import channels.layers
from asgiref.sync import async_to_sync
import common.saas as saas
import pytz

from app.db.db_patch import SaasHandler
from common.views.view import SampleAPIView
from rest_framework.response import Response
from common.web.json import JsonResult
from common.permission.controller import UserRoleAuthenticated
import common.sql as Sql
from rest_framework import authentication, permissions, serializers
from master.data.system import SystemConfig
from master.models.reserve import Reserve

class ReserveController(SampleAPIView):
    permission_classes = (UserRoleAuthenticated,)
    def fetch_reserve(self, request, *args, **kwargs):
        sql_condition = []

        params = {
            'current_date': datetime.combine(datetime.now().date(), datetime.min.time()),
            'status': request.data.get('status')
        }
        if request.data.get('status') != '1':
            
            sql_condition.append(
                    " AND status = '0' ")
        sql = """
            SELECT * FROM reserve WHERE 1 = 1 
                AND reserve_date >= %(current_date)s
                {0}
                ORDER BY reserve_date ASC, id ASC
            """
        result = JsonResult(data=Sql.sql_to_dict(sql.format('\n'.join(sql_condition)), params), message='ok')
        return Response(result)

    def update_reserve(self, request, *args, **kwargs):
        re = Reserve.objects.get(pk=request.data['id'])
        re.status = request.data['status']
        re.save()
        return Response(data={}, status=200)

class ReserveClientController(SampleAPIView):
    permission_classes = (permissions.AllowAny,)
    def add_reserve(self, request, *args, **kwargs):
        reserve = Reserve.objects.create(**request.data)

        utc_time = datetime.strptime(reserve.reserve_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        utc_time = utc_time.replace(tzinfo=pytz.UTC)
        jst = pytz.timezone('Asia/Tokyo')
        jst_time = utc_time.astimezone(jst)
        formatted_date_time = jst_time.strftime('%m-%d %H:%M')
        

        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            saas.group_name(saas.id(request), '__ReserveConsumer__'),
            {
                'type': 'send_message',
                'data': {
                    "message": f"新しい予約が入りました ({formatted_date_time})",
                }
            })
        return Response(data=request.data, status=200)

    def fetch_shop(self, request, *args, **kwargs):
        remote_addr = request.META.get('HTTP_X_REAL_IP')
        if remote_addr is None:
            remote_addr = request.META.get('REMOTE_ADDR')
        print(remote_addr, "----")
        data = {
            'plugin': SaasHandler.get_plugin(),
            'shop_detail': SaasHandler.get_shopDetail(),
        }

        result = JsonResult(data=data)

        return Response(result)

    
