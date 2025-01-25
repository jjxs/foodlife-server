from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import authentication, permissions, serializers

from master.models.guest import Guest, GuestUser
from master.models.seat import Seat, SeatStatus
from master.serializer.seat import SeatSerializer, SeatStatusSerializer

from common.util import Util
from common.log import logger
from common.web.json import JsonResult
from common.views.view import SampleAPIView
from common.permission.controller import UserRoleAuthenticated
import common.sql as Sql

import master.data.cache_data as cache_data


class MangementController(SampleAPIView):
    # 認証
    permission_classes = (UserRoleAuthenticated,)

