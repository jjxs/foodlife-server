from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from master.models.order import *
from master.serializer.order import *
from common.permission.controller import UserRoleAuthenticated
from common.filter import CharInFilter
from common.web.json import JsonResult

# SeatGroup　ONLY


class OrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = ('__all__')


class OrderController(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)

    queryset = Order.objects.all().order_by('-order_time')

    serializer_class = OrderSerializer

    filter_class = OrderFilter
