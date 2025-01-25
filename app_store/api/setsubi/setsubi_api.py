
import datetime
from urllib import request
from zipfile import is_zipfile

from botocore import model
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
import app.util as Util
from app.db.models.store_table import (
    AuthGroup, AuthUserGroups, AuthMenu, Machine)
from app.exception.web import WebException
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from common.web.json import JsonResult
from rest_framework.response import Response


class SetsubiApi(BaseAPI):

    def set_setsubi_data(self, request, params):
        # MAC_ID为空为PC端
        if 'MAC_ID' in params and not params['MAC_ID']:
            return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

        '''データ保存'''
        DATA_BASE = 'ami'

        result = Machine.objects.filter(sign=params['MAC_ID'])

        machine_status = False
        if(len(result) == 0):
            machine = Machine()
            machine.id = machine.next_value()
            machine.sign = params["MAC_ID"]
            machine.update_data = datetime.datetime.now()
            machine.save()
        else:
            machine = Machine.objects.using(
                DATA_BASE).get(pk=result[0].id)
            machine.last_data = datetime.datetime.now()
            machine.save()
            
            machine_status = machine.status
        
        
        if not machine_status:
            result = JsonResult(
                result=False, message="該当設備はまだ承認していません。管理者に連絡してください。")
            return Response(result)
        else:
            return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))
    
    # 設備使用
    def bind(self, request, params):
        if not self.check_bind():
            result = JsonResult(
                result=False, message="該当設備は使用できません。管理者に連絡してください。")
            return Response(result)
        else:
            machine = Machine.objects.get(pk=params["id"])
            machine.status = True
            machine.save()
            return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    # check config
    def check_bind(self):
        result_machine_mun = Machine.objects.filter(status=True).count()
        print(result_machine_mun)
        machine_config_num = self.machine_config_num()

        return machine_config_num > result_machine_mun

    def machine_config_num(self):
        '''データ保存'''
        DATA_BASE = 'ami'

        result = []

        sql_config_mun = '''
        SELECT
            value
        FROM master_config
        WHERE
            key = 'license'
            '''
        # master_config → license
        result_config = SQL.sql_to_list(
            sql=sql_config_mun, params={}, DB_name=DATA_BASE)

        result_config_mun = 0
        if len(result_config) > 0:
            result_config_mun = int(result_config[0]['value']['machine_count'])
        return result_config_mun

    def get_setsubi_data(self, request, params):
        '''データ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            id,
            sign,
			status,
            update_data,
            last_data
        FROM machine
        WHERE 1=1
            {0}
        ORDER BY update_data
        '''
        if 'keyword' in params and params['keyword']:
            sql_condition.append(
                ' AND (sign LIKE %(keyword)s)'
            )
            sql_param['keyword'] = '%' + params['keyword'] + '%'

        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_list(
            sql=sql, params=sql_param, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def del_setsubi_data(self, request, params):
        '''ユーザーデータ削除'''

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                machine = Machine()
                params['status'] = False
                machine = Machine.objects.using(
                    DATA_BASE).get(pk=params['id'])
                machine.save(request=request, using=DATA_BASE, values=params)

                sql_machine = '''
                SELECT
                    *
                FROM machine
                WHERE
                    status = false
                AND sign != %(sign)s
                order by update_data
                '''

                # result_machine = SQL.sql_to_list(
                #     sql=sql_machine, params={'sign': params['sign']}, DB_name=DATA_BASE)

                # if len(result_machine) > 0:
                #     machine = Machine.objects.using(
                #         DATA_BASE).get(pk=result_machine[0]['id'])
                #     params = result_machine[0]
                #     params["status"] = True
                #     machine.save(request=request,
                #                  using=DATA_BASE, values=params)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_mac_data(self, request, params):
        DATA_BASE = 'ami'
        # 先查询メニュー当前机器的MAC是否处于激活状态
        # MACID = "CD:F7:35:95:92:5E"
        MACID = request.data['__mac']
        if MACID != '':
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
            result_MAC = SQL.sql_to_list(
                sql=sql_MAC, params={'MAC_ID': MACID}, DB_name=DATA_BASE)
            if len(result_MAC) == 0:
                return JsonResponse(result=False, data='')

        return JsonResponse(result=True, data='1')
