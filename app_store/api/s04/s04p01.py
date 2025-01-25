
from os.path import basename

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
from app.auth.backend import WebException
from app.db.models.mst import MstStock
from app.db.models.tbl import TblIssue
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.models import MstUser


class S04p01Api(BaseAPI):

    # 出庫データ取得する
    def get_issue_info(self, request, params):

        result = self.get_issue_info_data()
        return JsonResponse(result=True, data=result)

    def get_issue_info_data(self):

        # 出庫リストデ－タ取得

        sql = '''
        SELECT
            mst.id,
            mst.part_name,
            mst.parts_type,
            mst.part_unit
        FROM
            mst_parts mst
            inner join mst_stock on mst.id = mst_stock.part_id
        ORDER BY
            mst.part_code
        '''

        result = SQL.sql_to_list(sql=sql)

        return result

        # 拠点データ取得する
    def get_base_info(self, request, params):

        result = self.get_base_info_data()
        return JsonResponse(result=True, data=result)

    def get_base_info_data(self):

        # 拠点リストデ－タ取得

        sql = '''
        SELECT
            mst.id,
            mst.base_name
        FROM
            mst_base mst
            inner join mst_stock on mst.id = mst_stock.base
        '''

        result = SQL.sql_to_list(sql=sql)

        return result

    # 検索ボタン押下
    def get_issue_data(self, request, params):

        result = self.get_issue_data_info(params, request.user)
        return JsonResponse(result=True, data=result)

    def get_issue_data_info(self, request_param, user):

        sql_condition = []
        sql_param = {}
        # 主役組織
        if "issue_date" in request_param and request_param["issue_date"]:
            sql_condition.append("AND A.issue_date = %(issue_date)s")
            sql_param["issue_date"] = request_param["issue_date"]

        if "part_id" in request_param and request_param["part_id"]:
            sql_condition.append("AND A.part_id::TEXT LIKE %(part_id)s")
            sql_param["part_id"] = "%" + request_param["part_id"] + "%"

        if "part_name" in request_param and request_param["part_name"]:
            sql_condition.append("AND B.part_name LIKE %(part_name)s")
            sql_param["part_name"] = "%" + request_param["part_name"] + "%"

        if "parts_type" in request_param and request_param["parts_type"]:
            sql_condition.append("AND B.parts_type::TEXT LIKE %(parts_type)s")
            sql_param["parts_type"] = "%" + request_param["parts_type"] + "%"

        result = SQL.sql_to_page("store.s04.mst_issue",
                                 sql_param, ['\n'.join(sql_condition)], request_param)

        return result

    # 保存ボタンを押下する
    def get_data_click(self, request, params):

        with transaction.atomic():
            try:
                tbl_issue = TblIssue()
                tbl_issue.insert(values=params, request=request)
                mst_stock = MstStock.objects.get(
                    part_id=params["part_id"], base=int(params['base']))
                mst_stock.parts_inventory_qty = mst_stock.parts_inventory_qty - \
                    int(params['goods_issue_quantity'])
                mst_stock.save(request=request)
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00023)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    #　明細デ－タ収集する
    def get_issue_detail_data(self, request, params):

        sql_param = {}
        result = []

        if "id" in params and params["id"]:
            sql_param["id"] = params["id"]
            result = SQL.sql_to_list(
                sql_id="store.s04.mst_issue_detail", params=sql_param)

        data = result[0] if result else {}

        return JsonResponse(result=True, data=data)

    # 削除ボタンを押下する
    def get_delete_data(self, request, params):
        with transaction.atomic():
            try:
                if params["id"]:
                    tbl_issue = TblIssue.objects.get(pk=params["id"])
                    tbl_issue.delete()
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00023)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))
