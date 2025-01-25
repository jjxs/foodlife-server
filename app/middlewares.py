from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from common.web.json import JsonResult
import app.db.sql as SQL

from django.http import HttpResponse
import json
from django.db.utils import ConnectionHandler

from app.db.db_patch import SaasHandler
import common.saas as saas
from django.db import connections

class Mac(MiddlewareMixin):
    

    def process_request(self, request):
        mac_id = request.GET.get('__mac')
        
        # SAASモード　対応
        connections.close_all()
        SaasHandler.set_saas_id(saas.id(request))
        path_info = request.META["PATH_INFO"]
        
        SQL.sql_to_list(sql="SELECT 1")

        print(SaasHandler.get_status())
        if not SaasHandler.get_status():
            result = {'result': False, 'message': "システムエラー", 'data': ''}
            return HttpResponse( json.dumps(result) )
        print(path_info, mac_id)
        if mac_id and mac_id != '' and path_info!="/login/" and SaasHandler.get_saas_id()!="" and path_info!="/s/setsubi_api/set_setsubi_data/" and path_info!='/test/':
            sql_MAC = '''
                SELECT
                    *
                FROM machine
                WHERE
                    status = true
                AND
                    sign = %(MAC_ID)s
            '''
            # データ重複かどうか
            result = SQL.sql_to_list(sql=sql_MAC, params={'MAC_ID': mac_id})
            if len(result) == 0:
                result = {'result': False, 'message': "MAC无效！失敗しました！", 'data': ''}
                return HttpResponse( json.dumps(result) )
