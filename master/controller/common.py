from io import BytesIO
from os.path import join
import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from rest_framework import authentication, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

import app.db.sql as SQL
import web.settings as settings
from common.log import logger
from common.util import Util
from common.views.view import SampleAPIView
from common.web.json import JsonResult
from master.data.system import SystemConfig
from master.models.guest import Guest, GuestUser
from app.db.db_patch import SaasHandler


class QRController(SampleAPIView):

    permission_classes = (permissions.AllowAny,)

    def read(self, request, *args, **kwargs):
        result = False
        try:
            image = ContentFile(request.FILES['file'].read())
            # temp = Image.open(image)
            # data = decode(temp)
            # code = data[0][0].decode('utf-8', 'ignore')
            result = True
        except expression as identifier:
            pass

        result = JsonResult(result=result, data=code)

        return Response(result)


class InitController(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        
        if request.user is None:
            result = JsonResult(result=False, message="該当ユーザ存在していない。")
            return Response(result)
        # user
        resultdata = {}
        user_id = request.user.id
        DATA_BASE = 'ami'
        # user → first_name last_name is_supperuser is_staff nickname display_name
        result_user = []
        result = []
        sql_user = '''
        SELECT
            id,
            username,
            first_name as display_name,
            CONCAT(first_name ,' ',last_name) as nickname,
            is_superuser,
            is_staff,
            is_active
        FROM auth_user
        WHERE
            id = %(user_id)s
            '''

        result_user = SQL.sql_to_list(
            sql=sql_user, params={'user_id': user_id}, DB_name=DATA_BASE)
        for newresulr_user in result_user:
            guest_user = newresulr_user['username']
            if(newresulr_user['is_active'] == True):
                resultdata['no'] = newresulr_user['id']
                resultdata['nickname'] = newresulr_user['nickname']
                if(newresulr_user['is_superuser'] == True):
                    newresulr_user['display_name'] = "システム管理者"
                elif(newresulr_user['is_staff'] == True):
                    newresulr_user['display_name'] = "スタッフ"
                else:
                    newresulr_user['display_name'] = "ゲスト"
                resultdata['role'] = newresulr_user
            else:
                result = JsonResult(result=False, message="該当ユーザ有効しない。")
        if guest_user == "guest":
            resultdata['nickname'] = "guest"
            resultdata['auth_menu'] = [ {'menu_path':'/menu'} ]
            resultdata['role']['guest'] = True
            result = JsonResult(
                result=True, message="guest取得しました！", data=resultdata)
            return Response(result)

        # group_id → menu_list
        allow_menu_path = self.get_allow_path(user_id)
        resultdata["auth_menu"] = allow_menu_path

        # 输入的menu在当前组的里边，可
        if self.check(request, allow_menu_path):
            result = JsonResult(
                result=True, message="取得しました！", data=resultdata)
        else:
            result = JsonResult(
                result=True, message="取得失敗しました！画面権限がありません！", data='')

        return Response(result)
    
    def get_allow_path(self, user_id):
        sql_menu = '''
            SELECT
                AM.menu_path
            FROM auth_menu AM
            LEFT JOIN auth_user_groups AUG ON AUG.group_id = AM.group_id
            WHERE
                AUG.user_id = %(user_id)s
            '''
        result = SQL.sql_to_list(sql=sql_menu, params={'user_id': user_id})
        allow_path = []
        allow_path.append({'menu_path': '/'})
        for row in result:
            if row['menu_path'] not in allow_path:
                allow_path.append({'menu_path': row['menu_path']} )
        return allow_path

    def check(self, request, allow_menu_path):
        return True
        # 获取的地址 判断输入的地址所在的menu是否有权限进行查看
        current_path = self.get_http_referer(request)
        for row in allow_menu_path:
            path = row['menu_path']
            if path==current_path:
                return True

        return False
        # (current_path in allow_menu_path)

    def get_http_referer(self, request):
        referer = request.META.get('HTTP_REFERER')
        if not referer:
            return default

        # remove the protocol and split the url at the slashes
        referer = re.sub('^https?:\/\/', '', referer).split('/')
        path = '/'
        if len(referer)>1:
            # add the slash at the relative path's view and finished
            path = u'/' + u'/'.join(referer[1:])
        
        # 库中存的是/menu/,需要转换
        err_path = '/store/setsubi-error'
        if(path == '/menu'):
            path = '/menu/'
        elif len(path)>len(err_path) and path[0:len(err_path)]==err_path:
            path = '/'
        elif len(path)>=8 and path[0:8]=='/manager':
        # 如果是从子页面进入的，就只有manager有子页面，也可
            path = '/manager'
        elif len(path)>=6 and path[0:6]=='/staff':
            path = '/staff'
        return path


class AppController(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        remote_addr = request.META.get('HTTP_X_REAL_IP')
        if remote_addr is None:
            remote_addr = request.META.get('REMOTE_ADDR')
        print(remote_addr, "----")
        data = {
            "system_name": SystemConfig.system_name(),
            "fax": SystemConfig.fax(),
            "takeout_fax": SystemConfig.takeout_fax(),
            "version": SystemConfig.version(),
            "shopInfo": SystemConfig.shop_info(),
            "siteImageHost": settings.SITE_IMAGE_HOST,
            'plugin': SaasHandler.get_plugin(),
            'whitelist': SystemConfig.whitelist(remote_addr),
            'qrtheme': SystemConfig.qrtheme()
            # 'shopInfo': {
            #     'addr1': '東京都台東区上野4丁⽬4-5',
            #     'addr2': '上野C-Roadビル 3F',
            #     'tel'  : '03-6806-0583',
            #     'post' : '〒110-0005',
            #     'time1': '11:30am~15:00pm',
            #     'time2': '17:30pm~23:00pm'
            # }
        }

        result = JsonResult(data=data)

        return Response(result)
