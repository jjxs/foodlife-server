from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from django_filters import rest_framework as filters

from master.models.seat import SeatGroup
from master.serializer.seat import *
from common.permission.controller import UserRoleAuthenticated
from common.filter import NumberInFilter
from common.web.json import JsonResult

# SeatGroup　ONLY


class SeatGroupFilter(filters.FilterSet):
    class Meta:
        model = SeatGroup
        fields = ('no', 'name', 'start')


class SeatGroupController(viewsets.ModelViewSet):

    permissions = (UserRoleAuthenticated,)

    queryset = SeatGroup.objects.all().order_by('no')

    serializer_class = SeatGroupSerializer

    filter_class = SeatGroupFilter


class SeatStatusFilter(filters.FilterSet):
    class Meta:
        model = SeatStatus
        fields = ('__all__')


class SeatStatusController(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)

    queryset = SeatStatus.objects.all()

    serializer_class = SeatStatusSerializer

    filter_class = SeatStatusFilter


class SeatFilter(filters.FilterSet):

    id__in = NumberInFilter(field_name="id", lookup_expr="in")
    takeout = filters.NumberFilter(field_name="takeout_type")

    class Meta:
        model = Seat
        fields = ('id', 'id__in', 'takeout')


class SeatController(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)

    queryset = Seat.objects.all().order_by('group_no', 'seat_no')

    serializer_class = SeatSerializer

    filter_class = SeatFilter

    def list(self, request):

        request = self.request
        if 'using' in request.GET:
            sql = '''
            select seat.* from seat 
            inner join seat_status on seat_status.seat_id = seat.id
            where 1 = 1 {0}
            order by seat_no
            '''
            array = []
            sql_format = ''
            sql_params = {}

            if 'id' in request.GET:
                array.append(request.GET['id'])

            if 'id__in' in request.GET:
                for id in tuple(request.GET['id__in']):
                    #TODO:　一時対策
                    if id.isdigit():
                        array.append(id)

            if len(array) > 0:
                sql_format = ' and seat.id in %(ids)s '
                sql_params = {'ids': tuple(array)}

            if 'takeout' in request.GET and request.GET['takeout']:
                sql_format = ' and seat.takeout_type = 1'
            else:
                sql_format = ' and (seat.takeout_type is null  or seat.takeout_type = 0)'
            queryset = Seat.objects.raw(sql.format(sql_format), sql_params)
        else:
            queryset = Seat.objects.all().order_by('seat_no')
            queryset = self.filter_queryset(queryset)

        serializer = SeatSerializer(queryset, many=True)

        return Response(serializer.data)


    # def get_queryset(self):

    #     request = self.request
    #     if 'using' in request.GET:
    #         queryset = Seat.objects.raw('''
    #         select seat.* from seat
    #         inner join seat_status on seat_status.seat_id = seat.id
    #         order by seat_no
    #         ''')
    #     else:
    #         queryset = Seat.objects.all().order_by('seat_no').all()
    #     return queryset
