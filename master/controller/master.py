from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
# from django.core.cache import cache

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from master.models.master import MasterData, MasterDataGroup
from master.serializer.master import MasterSerializer,  MasterDataSerializer, MasterDataGroupSerializer
from common.permission.controller import UserRoleAuthenticated
from common.filter import CharInFilter
from common.web.json import JsonResult
import master.data.cache_data as cache
# MasterData　ONLY


class MasterDataFilter(filters.FilterSet):
    group__name__in = CharInFilter(name="group__name", lookup_expr="in")
    # group_id = filters.NumberFilter(name="group__id", lookup_expr="exact")

    class Meta:
        model = MasterData
        fields = {'group__name'}
        # fields = {
        #     'group__id': ['exact'],
        #     'group__name': ['startswith'],
        #     'group': ['exact'],
        #     'code': ['exact'],
        #     'id': ['exact']
        # }


class MasterDataController(viewsets.ModelViewSet):

    permissions = (UserRoleAuthenticated,)

    queryset = MasterData.objects.all().order_by('display_order')

    serializer_class = MasterDataSerializer

    filter_class = MasterDataFilter


# MasterDataGroup　ONLY
class MasterDataGroupFilter(filters.FilterSet):
    class Meta:
        model = MasterDataGroup
        fields = ['id', 'name', 'domain', 'enabled']


class MasterDataGroupController(viewsets.ModelViewSet):

    permissions = (UserRoleAuthenticated,)

    queryset = MasterDataGroup.objects.all().order_by('domain', 'display_order')

    serializer_class = MasterDataGroupSerializer

    filter_class = MasterDataGroupFilter


# MasterDataGroup　+ DataList
# class MasterController(APIView):

#     # 認証
#     permission_classes = (UserRoleAuthenticated,)

#     #
#     def get(self, request, format=None):

#         groups = MasterDataGroup.objects.all()
#         data = MasterSerializer(groups, many=True)
#         result = JsonResult(data.data)

#         return Response(result)


class MasterFilter(filters.FilterSet):

    name__in = CharInFilter(field_name="name", lookup_expr="in")
    domain__in = CharInFilter(field_name="domain", lookup_expr="in")

    class Meta:
        model = MasterDataGroup
        fields = ['id', 'name', 'domain', 'name__in', 'domain__in', 'enabled']


class MasterController(viewsets.ModelViewSet):

    permissions = (UserRoleAuthenticated,)

    queryset = MasterDataGroup.objects.all().order_by('display_order')


    serializer_class = MasterSerializer

    filter_class = MasterFilter

    def get_cache_key(self, params):

        domain = params["domain"] if "domain" in params else "None"
        name = params["name"] if "name" in params else "None"
        master_id = params["id"] if "id" in params else "None"
        name__in = params["name__in"] if "name__in" in params else "None"
        domain__in = params["domain__in"] if "domain__in" in params else "None"
        enabled = params["enabled"] if "enabled" in params else "None"

        key = "{0}||{1}||{2}||{3}||{4}||{5}".format(domain, name, master_id, name__in, domain__in, enabled)
        return key

    def filter_queryset(self, queryset):

        # キャッシュを利用するため、カスタマイズ
        key = self.get_cache_key(self.request.query_params)
        cachedata = cache.cache_get('master_data')

        if cachedata is None:
            cachedata = {}

        if key in cachedata:
            print("master_data cache used!!")
            return cachedata[key]

        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        # cachedata[key] = queryset
        # cache.cache_set('master_data', cachedata)
        return queryset
