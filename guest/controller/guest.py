import django_filters
from rest_framework import viewsets, permissions
from common.log import logger
from common.permission.controller import UserRoleAuthenticated

from master.models.guest import Guest, GuestDevice, GuestGroup, GuestUser
from master.serializer.guest import GuestDataSerializer, GuestSerializer, GuestDeviceSerializer


class GuestFilter(django_filters.FilterSet):

    class Meta:
        model = Guest
        fields = ['id', 'no', 'nickname']

# Guest Data ONLY
class GuestDataController(viewsets.ModelViewSet):
    permission_classes = (UserRoleAuthenticated,)

    queryset = Guest.objects.all()
    serializer_class = GuestDataSerializer
    filter_class = GuestFilter

# Device Data ONLY
class GuestDeviceController(viewsets.ModelViewSet):
    permission_classes = (UserRoleAuthenticated,)

    queryset = GuestDevice.objects.all()
    serializer_class = GuestDeviceSerializer
    filter_class = GuestFilter

# Guest Data with device list and user list
class GuestController(viewsets.ModelViewSet):
    permission_classes = (UserRoleAuthenticated,)

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_class = GuestFilter
