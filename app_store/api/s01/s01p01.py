
import app.db.sql as SQL
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from app.auth.backend import WebException
from app.db.models.tbl import TblWarehousing
from app.db.models.tbl import TblWarehousingDetail
import app.const as Const
import app.common.message as Message


class S01p01Api(BaseAPI):

    # 検索ボタン押下
    def get_data(self, request, params):

        result = self.get_data_info(params, request.user)
        return JsonResponse(result=True, data=result)

    def get_data_info(self, request_param, user):

        sql_condition = []
        sql_param = {}
        # 主役組織
        if "receipt_date" in request_param and request_param["receipt_date"]:
            sql_condition.append(
                "AND A.receipt_date = %(receipt_date)s")
            sql_param["receipt_date"] = request_param["receipt_date"]

        if "part_name" in request_param and request_param["part_name"]:
            sql_condition.append("AND B.part_name LIKE %(part_name)s")
            sql_param["part_name"] = "%" + request_param["part_name"] + "%"

        if "receipt_id" in request_param and request_param["receipt_id"]:
            sql_condition.append("AND B.receipt_id::TEXT LIKE %(receipt_id)s")
            sql_param["receipt_id"] = "%" + request_param["receipt_id"] + "%"

        if "parts_type" in request_param and request_param["parts_type"]:
            sql_condition.append("AND A.parts_type = %(parts_type)s")
            sql_param["parts_type"] = request_param["parts_type"]

        if "parts_unit_price_tax_inc" in request_param and request_param["parts_unit_price_tax_inc"]:
            sql_condition.append(
                "AND B.parts_unit_price_tax_inc::TEXT = %(parts_unit_price_tax_inc)s")
            sql_param["parts_unit_price_tax_inc"] = request_param["parts_unit_price_tax_inc"]

        result = SQL.sql_to_page("store.s01.mst_warehousing",
                                 sql_param, ['\n'.join(sql_condition)], request_param)

        return result

    # 保存ボタンを押下する
    def save_click(self, request, params):

        with transaction.atomic():
            try:
                if params["id"]:
                    warehousing = TblWarehousing.objects.get(
                        pk=params["receipt_id"])
                    warehousing_detail = TblWarehousingDetail.objects.get(
                        pk=params["id"])
                    warehousing.save(values=params, request=request)
                    warehousing_detail.save(values=params, request=request)
                else:
                    warehousing = TblWarehousing()
                    warehousing.insert(values=params, request=request)
                    warehousing_detail = TblWarehousingDetail()
                    warehousing_detail.receipt_id = warehousing.id
                    warehousing_detail.insert(values=params, request=request)
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00023)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    #　明細デ－タ収集する
    def get_detail_data(self, request, params):

        sql_param = {}
        result = []

        if "id" in params and params["id"]:
            sql_param["id"] = params["id"]
            result = SQL.sql_to_list(
                sql_id="store.s01.mst_warehousing_detail", params=sql_param)

        data = result[0] if result else {}

        return JsonResponse(result=True, data=data)

    # 削除ボタンを押下する
    def get_detail_delete_data(self, request, params):

        with transaction.atomic():
            try:
                if params["id"]:
                    warehousing = TblWarehousing.objects.get(
                        pk=params["receipt_id"])
                    warehousing_detail = TblWarehousingDetail.objects.get(
                        pk=params["id"])
                    warehousing.delete()
                    warehousing_detail.delete()
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00023)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))
