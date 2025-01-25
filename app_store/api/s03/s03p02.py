
from builtins import object

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from urllib3 import request

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
from app.auth.backend import WebException
from app.db.models.mst import MstParts, MstStock, MstStockHistory
from app.db.models.tbl import TblInspection
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.models import MstUser
import copy


class S03p02Api(BaseAPI):

    # 検索ボタン押下
    def get_result_data(self, request, params):

        result = self.get_result_data_info(params, request.user)
        return JsonResponse(result=True, data=result)

    def get_result_data_info(self, request_param, user):

        sql_condition = []
        sql_param = {}
        part_id = []

        sql = '''
        SELECT
            ins.id,
            ins.part_id,
            ing.ing_name part_name,
            ins.part_cat,
            ins.part_type,
            cat.cat_name parts_type,
            ins.part_unit,
            ins.parts_unit_price,
            ins.parts_currency,
            ins.parts_inventory_qty,
            ins.inspection_date,
            ins.inspector,
            ins.inspection_result_confirmation,
            ins.remarks
        FROM
            tbl_inspection       ins
        LEFT JOIN
            mst_ingredients      ing ON ins.part_id = ing.id
        LEFT JOIN
            mst_ingredients_cat  cat ON ing.ing_cat_id = cat.id
        WHERE
            ins.inspection_delete = 0
        OR
            ins.inspection_delete IS NULL
            {0}
        ORDER BY
            ins.id
        '''

        # if "id" in request_param and request_param["id"]:
        #     sql_condition.append("AND B.part_name LIKE %(id)s")
        #     sql_param["id"] = "%" + request_param["id"] + "%"

        # sql = SQL.get_sql("store.s03.mst_result_info").format(
        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_list(sql=sql, params=sql_param)
        print(result)

        sql = '''
            SELECT
                menu.id,
                menu.name
            FROM tbl_inspection ins 
            INNER JOIN menu on ins.part_id = menu.id
            WHERE ins.part_type = 2 
            '''
        result_menu = SQL.sql_to_list(sql=sql, params=sql_param)
        sql = '''
            SELECT
                md.id,
                coalesce(md.display_name, md.name) AS name
            FROM tbl_inspection ins 
            INNER JOIN master_data md on ins.part_cat = md.id
            WHERE ins.part_type = 2 
            '''
        result_cat = SQL.sql_to_list(sql=sql, params=sql_param)
        map_menu = {}
        for item in result_menu:
            map_menu[item['id']] = item['name']
        map_cat = {}
        for item in result_cat:
            map_cat[item['id']] = item['name']
        for item in result:
            if item['part_type']==2:
                if item['part_id'] in map_menu:
                    item['part_name'] = map_menu[item['part_id']]
                if item['part_cat'] in map_cat:
                    item['parts_type'] = map_cat[item['part_cat']]

        return result

    def save_click(self, request, params):

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                rows = params["rows"]
                for row in rows:
                    result = MstStock.objects.using(DATA_BASE).filter(part_id=row['part_id'])
                    if len(result):
                        stock = result[0]
                        item = copy.copy(row)
                        item['id'] = stock.id
                        stock.save(values=item, request=request)
                    else:
                        stock = MstStock()
                        stock.insert(request=request, values=row)
                    
                    # 履歴
                    stockHistory = MstStockHistory()
                    stockHistory.save(stock.__dict__)

                    inspection = TblInspection.objects.using(DATA_BASE).get(pk=row['id'])
                    inspection.inspection_delete = 1
                    inspection.save(values=row, request=request)
                
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00023)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))
