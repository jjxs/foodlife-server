
import app.db.sql as SQL
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.models import MstUser
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from app.auth.backend import WebException
from app.db.models.tbl import TblWarehousing
from app.db.models.tbl import TblWarehousingDetail
import app.const as Const
import app.common.message as Message


class S02p01Api(BaseAPI):

    # 検索ボタン押下
    def get_data(self, request, params):

        result = self.get_data_info(params, request.user)
        return JsonResponse(result=True, data=result)

    def get_data_info(self, request_param, user):

        sql_condition = []
        sql_param = {}
        
        # 主役組織
        if "order_date" in request_param and request_param["order_date"]:
            sql_condition.append("AND A.order_date = %(order_date)s")
            sql_param["order_date"] = request_param["order_date"]

        if "order_number" in request_param and request_param["order_number"]:
            sql_condition.append("AND A.order_number LIKE %(order_number)s")
            sql_param["order_number"] = "%" + request_param["order_number"] + "%"

        sql = SQL.get_sql("store.s02.mst_order").format('\n'.join(sql_condition))
        result = SQL.sql_to_list(sql=sql, params=sql_param)

        return result

