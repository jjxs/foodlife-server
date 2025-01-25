
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

import app.const as Const
import app.util as Util
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.exception.web import WebException
from app.db.models.mst import MstStore, MstOrganization
from app.db.models.tbl import TblStoreSiteInfo


class StoreRegApi(BaseAPI):

    def init_data(self, request, params):
        '''画面初期化'''

        states = Util.get_code(Const.CodeTypes.TYPE_2)

        data = {
            'states': states
        }

        return JsonResponse(result=True, data=data)

    def set_data(self, request, params):

        store_info_param = params['info']
        store_site_param = params['site']

        with transaction.atomic():
            try:
                # 店舗を組織マスタにも入れておく
                store_org = MstOrganization()
                store_org.insert(request=request)
                store_org.org_code = store_info_param['store_code']
                store_org.org_name = store_info_param['store_name']
                store_org.upper_organization_id = 0
                store_org.org_hierarchy_path = '/' + store_org.pk +'/'
                store_org.phone_number = store_info_param['phone_number']
                store_org.save()

                # 店舗基本情報保存
                store = MstStore()
                store.store_org_id = store_org.pk
                store.insert(request=request, values=store_info_param)

                # 店舗サイト情報保存
                store_site = TblStoreSiteInfo()
                store_site.store_id = store.pk
                store_site.insert(request=request, values=store_site_param)
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True)
