
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

import base64
import os
import boto3

import app.const as Const
import app.common.message as Message
import app.db.sql as SQL
import web.settings as settings
import app.util as Util
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.exception.web import WebException
from app.db.models.store_table import MasterData, MasterDataGroup
from django.db.models import Max
from app.db.db_patch import SaasHandler


class PaymentApi(BaseAPI):

    def get_ing_data(self, request, params):
        '''支払方法データ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            id, 
            code,
            name,
            display_name,
            display_order,
            option
        FROM 
            master_data
        WHERE 
            group_id = 15
            {0}
        ORDER BY
            code
        '''

        if 'keyword' in params and params['keyword']:
            sql_condition.append(
                'AND (display_name LIKE %(keyword)s)'
            )
            sql_param['keyword'] = '%' + params['keyword'] + '%'

        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_list(sql=sql, params=sql_param, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def get_edit_data(self, request, params):
        '''編集フォームのデータ取得'''

        data = []

        DATA_BASE = 'ami'

        if 'id' in params and params['id']:
            sql = '''
            SELECT
                id,
                code,
                name,
                display_name,
                display_order,
                option
            FROM
                master_data
            WHERE
                id = %(id)s
            '''

            result = SQL.sql_to_list(
                sql=sql, params={'id': params['id']}, DB_name=DATA_BASE)

            data = {
                'rows': result,
                'site_image_host': settings.SITE_IMAGE_HOST
            }

        return JsonResponse(result=True, data=data)

    def set_ing_data(self, request, params):
        '''支払方法データ保存'''

        DATA_BASE = 'ami'

        if 'edit_flag' in params and params['edit_flag']:
            if params['edit_flag'] == 0:
                # 支払方法名称重複チェック
                exist = self.check_exist_payment_name(params)
                if exist:
                    return JsonResponse(result=False, message='入力された名前がすでに存在します')
        params['group_id'] = 15;
        if not params['code']:
            params['code'] = self.get_code()
        with transaction.atomic(using=DATA_BASE):
            try:
                if 'id' in params and params['id']:
                    ing = MasterData.objects.using(
                        DATA_BASE).get(pk=params['id'])
                    ing.save(request=request, values=params, using=DATA_BASE)

                else:
                    ing = MasterData()
                    ing.insert(request=request, values=params, using=DATA_BASE)

                master_id = ing.pk

                # メニュー画像保存
                if "imgData" in params and params["imgData"]:
                    file_name = '/payment_images/' + params["imgName"]

                    # ファイル作成
                    file_info = str(params["imgData"])
                    _, b64data = file_info.split(',')

                    s3 = boto3.resource('s3')
                    image_url = SaasHandler.get_saas_id() + file_name
                    s3.Bucket('foodlife').put_object(
                        Key=image_url, Body=base64.b64decode(b64data), ACL="public-read")
                    newoption = {}
                    newoption['img'] = image_url
                    ing.option = newoption
                    ing.save()

                elif "imgData" in params and not params["imgData"]:
                    # ort_path = settings.STATIC_ROOT + menu.image
                    # if os.path.exists(ort_path):
                    #     os.remove(ort_path)

                    # s3 = boto3.resource('s3')
                    # s3.Bucket('foodlife').put_object(Key=menu.image)
                    ing.image = ''
                    ing.save()

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005), data=master_id)

    def get_code(self):
        code = MasterData.objects.filter(group_id=15).aggregate(Max('code'))[
            'code__max'] or 0
        return code + 1

    def check_exist_payment_name(self, params):
        '''重複チェック'''

        DATA_BASE = 'ami'
        sql_param = {}
        sql_condition = []

        sql = '''
        SELECT
            COUNT(0)
        FROM
            master_data master
        WHERE
            master.name = %(name)s
            {0}
        '''

        sql_param['name'] = params['name']

        if 'master_id' in params and params['master_id']:
            sql_condition.append(' AND master.id != %(master_id)s ')
            sql_param['master_id'] = params['master_id']

        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_one(sql=sql, params=sql_param, DB_name=DATA_BASE)

        if result > 0:
            return True
        else:
            return False

    def delete_ing_data(self, request, params):
        '''支払方法データ削除'''

        DATA_BASE = 'ami'
        with transaction.atomic(using=DATA_BASE):
            try:
                for row in params['rows']:
                    ing = MasterData.objects.using(DATA_BASE).get(pk=row['id'])
                    ing.delete()
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))
