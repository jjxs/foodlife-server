from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import authentication, permissions, serializers

from master.models.guest import Guest, GuestUser
from master.models.seat import Seat, SeatStatus
from master.models.master import Config, Language
from master.serializer.seat import SeatSerializer, SeatStatusSerializer

from common.util import Util
from common.log import logger
from common.web.json import JsonResult
from common.views.view import SampleAPIView
from common.permission.controller import UserRoleAuthenticated
import common.sql as Sql

class MasterController(SampleAPIView):
    # 認証
    permission_classes = (UserRoleAuthenticated,)

    # 遅い処理をSQL＋キャッシュ化する
    def post_config(self, request, *args, **kwargs):
        configs = Config.objects.filter(key=request.data['key'])
        config = Config()
        if len(configs)>0:
            config = configs[0]
        config.key = request.data['key']
        config.value = request.data['value']
        config.save()
        result = {
            'id' : config.id,
            'message': '処理しました。'
        }
        return Response(result)

    # 遅い処理をSQL＋キャッシュ化する
    def config(self, request, *args, **kwargs):
        configs = Config.objects.filter(key=request.GET['key'])
        config = Config()
        if len(configs)>0:
            config = configs[0]
        result = {
            'config' : {
                'key': config.key,
                'value': config.value
            },
            'message': '処理しました。'
        }
        return Response(result)
    
    def language(self, request, *args, **kwargs):
        sql_param = {}
        sql_condition = []

        sql = '''
            SELECT *
            FROM master_language
            WHERE 1 = 1
            {0}
            ORDER BY id DESC
        '''
        if 'keyword' in request.data and request.data['keyword']:
            sql_condition.append(
                'AND (name LIKE %(keyword)s)'
            )
            sql_param['keyword'] = '%' + request.data['keyword'] + '%'
        sql = sql.format('\n'.join(sql_condition))
        result = Sql.sql_to_dict(sql=sql, params=sql_param)
        return Response(result)
        
    def post_language(self, request, *args, **kwargs):
        if 'key' in request.data:
            for k in request.data['key']:
                obj = Language()
                languages = Language.objects.filter(name=k)
                if len(languages)>0:
                    obj = languages[0]
                obj.name = k
                obj.ja = k
                obj.save()
        return Response({})
    
    def delete_language(self, request, *args, **kwargs):
        Language.objects.filter(pk=request.data["id"]).delete()
        return Response({})
    
    def check_psss(self, request, *args, **kwargs):
        configs = Config.objects.filter(key='pad_secret_key', value=request.data['password'])
        status = 0
        if len(configs)>0:
            status = 1
        result = {
            'status': status
        }
        return Response(result)

    def update_language(self, request, *args, **kwargs):
        if 'name' not in request.data:
            return Response({})
            
        obj = Language()
        languages = Language.objects.filter(name=request.data['ja'])
        if len(languages)>0:
            obj = languages[0]
        obj.name = request.data['ja']
        obj.ja = request.data['ja']
        obj.en = request.data['en']
        obj.zh = request.data['zh']
        obj.save()
        return Response({'data':request.data})
