from django.db import transaction
from rest_framework import authentication, permissions, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

import common.sql as Sql
import xxsubtype
from common.log import logger
from common.permission.controller import UserRoleAuthenticated
from common.util import Util
from common.views.view import SampleAPIView
from common.web.json import JsonResult
from master.models.guest import Guest, GuestUser
from master.models.master import Config
from master.models.menu import (Menu, MenuBind, MenuCourse, MenuCourseDetail,
                                MenuFree, MenuFreeDetail)
from app.db.models.store_table import (MenuTop)
import os
import boto3
import base64
from app.http.response import JsonResponse
import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
from app.db.db_patch import SaasHandler


class MenuTop3Controller(SampleAPIView):
    def set_menu_top3(self, request, *args, **kwargs):
        DATA_BASE = 'ami'
        sql_param = {}
        sql_condition = []
        data = request.data
        obj = MenuTop()
        # name
        file_name = data['imgName']
        menu_top = MenuTop()
        # 根据id进行更新
        # menu_top = MenuTop.objects.using(
        #     DATA_BASE).get(pk=data['id'])
        sql_res = '''
        SELECT
            *
            FROM menu_top
            WHERE
                menu_type = 'top3'
        '''
        result_res = SQL.sql_to_list(sql=sql_res, params=sql_param, DB_name=DATA_BASE)

        if(len(result_res) == 0):
            menu_top.id = menu_top.next_value()
        else:
            menu_top.id = data['id']
        if 'imgData' in data and data['imgData']:
            file_info = str(data["imgData"])
            _, b64data = file_info.split(',')

            s3 = boto3.resource('s3')
            menu_top.image = SaasHandler.get_saas_id() + '/theme/top3/' + file_name

            s3.Bucket('foodlife').put_object(
                Key=menu_top.image, Body=base64.b64decode(b64data), ACL="public-read")

        else:
            menu_top.image = ''

        menu_top.target_type = 'top3'
        menu_top.display_order = 0
        menu_top.menu_type = 'top3'
        menu_top.save()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_theme_list(self, request, *args, **kwargs):
        sql = '''
            SELECT *
            FROM menu_top where menu_type = 'top3'
        '''
        data = Sql.sql_to_dict(sql)
        result = {}
        if len(data):
            result = data[0]
        else:
            result = {
                'id': '',
                'image':''
            }
        return Response(result)
