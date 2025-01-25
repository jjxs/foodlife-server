
import app.db.sql as SQL
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.models import MstUser
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from app.auth.backend import WebException
from app.db.models.tbl import TblOrder
from app.db.models.tbl import TblOrderDetail
import app.const as Const
import app.common.message as Message


class S02p02Api(BaseAPI):

    # 検索ボタン押下
    def get_detail_data(self, request, params):

        result = self.get_detail_data_info(params, request.user)
        return JsonResponse(result=True, data=result)

    def get_detail_data_info(self, request_param, user):

        sql_condition = []
        sql_param = {}

        if 'id' in request_param:
            sql_param['id'] = request_param['id']

        # 主役組織        
        sql = SQL.get_sql("store.s02.mst_order_detail_save_click").format(
            '\n'.join(sql_condition))
        result = SQL.sql_to_list(sql=sql, params=sql_param)
        return result

    # 発注明細ボタン押下
    def set_orderdetail(self,request,params):

        with transaction.atomic():
            try:
                order = TblOrder()
                orderdata = params["OrderForm"]
                order.insert(values=orderdata,request=request)
                rows = params["rows"]
                for row in rows:
                    order_detail = TblOrderDetail()
                    order_detail.ordering_table_unique_id = order.id
                    order_detail.insert(values=row,request=request)

            except  ObjectDoesNotExist:
                raise  WebException(Const.MessageIDs.MQ00023)
        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))


              