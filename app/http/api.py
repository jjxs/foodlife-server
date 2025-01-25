
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from urllib.parse import urlparse
from datetime import datetime, date

from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_list_or_404 as _get_list_or_404
from rest_framework.permissions import BasePermission

# from base.auth.user import UserAuthenticated
from common.permission.controller import UserRoleAuthenticated

import json
import ast
from app.auth.token import AuthUser
import app.db.sql as SQL


def json_supporter(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(repr(obj) + "cannot seriializable")


class UserAuthenticated(BasePermission):

    def has_permission(self, request, view):
        print(request, request.user)
        # print("isinstance(request.user, AuthUser) and request.user.is_authenticated")
        # print(isinstance(request.user, AuthUser) and request.user.authenticated)
        return isinstance(request.user, AuthUser) and (request.user.authenticated)


class NoneAuthenticated(BasePermission):

    def has_permission(self, request, view):
        print("................. NoneAuthenticated ...............")
        return True


class BaseAPI(APIView):

    # 認証
    permission_classes = (UserRoleAuthenticated,)

    def to_json(self, obj):
        return json.dumps(obj, default=json_supporter)
        # Note: Views are made CSRF exempt from within `as_view` as to prevent
        # accidental removal of this exemption in cases where `dispatch` needs to
        # be overridden.

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """

        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)

        self.request = request
        self.headers = self.default_response_headers  # deprecate?
        querys = request.query_params
        data = request.data

        try:
            self.initial(request, *args, **kwargs)

            # 既存のGET,POSTをめっそど名の方式はBASEAPIで考慮しないようにする
            fun_name = self.kwargs.get('fun')
            params = {}
            response = {}
            class_name = self.__class__.__name__
            user_id = request.user.user_id if isinstance(request.user, AuthUser) else 0
            # SQL.execute('''
            #     INSERT INTO TBL_ACCESS_LOG(ID, API_NAME, METHOD_NAME, USER_ID, ACCESS_DATE) 
            #     VALUES (SEQ_TBL_ACCESS_LOG.NEXTVAL, %s,%s,%s, systimestamp)
            # ''', [class_name, fun_name, user_id])

            if request.method.lower() in self.http_method_names and fun_name:
                handler = getattr(self, str(fun_name).lower(),
                                  self.http_method_not_allowed)

                if request.method.lower() == 'get':
                    params = request.GET

                else:
                    params = request.data

                # 言語設定
                #request.auth_user.language = params["__language"]

                response = handler(request,  params)
            else:
                handler = self.http_method_not_allowed
                response = handler(request,  *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(
            request, response, *args, **kwargs)
        return self.response
