# coding=utf-8
import jwt
import traceback

from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser, User
from django.conf import LazySettings
from django.contrib.auth.middleware import get_user
from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from master.data.cache_data import *

settings = LazySettings()

from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
from app.db.db_patch import SaasHandler

# rest_framework のRequest自動設定されているため


def get_user_jwt(request):
    user = None
    err = None
    try:
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        try:
            payload = jwt_decode_handler(user_jwt[1])
            if 'saas_id' in payload and payload['saas_id']!=SaasHandler.get_saas_id():
                err = 'Signature has failed. site err'
        except jwt.ExpiredSignature:
            err = 'Signature has expired.'
        except jwt.DecodeError:
            err = 'Error decoding signature.'
        except jwt.InvalidTokenError:
            return None, exceptions.AuthenticationFailed()

        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except:
        pass

    return (user or AnonymousUser()), err


class AuthenticateMiddleware(MiddlewareMixin):

    
    print("*************** AuthenticateMiddleware ****************")
    def process_request(self, request):
        if request.content_type == "application/json":
            user, err = get_user_jwt(request)
            print(user, err)
            if err!=None:
                raise Exception(err)
            request.user = SimpleLazyObject(lambda: user)
            
            request.role = get_role(request.user)
            if not request.role:
                request.role = get_guest_role()
                
