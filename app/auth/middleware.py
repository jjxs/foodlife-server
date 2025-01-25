import jwt
import traceback

from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser, User
from django.conf import LazySettings
from django.contrib.auth.middleware import get_user
from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from app.auth.token import AuthUser, BaseTokenAuthentication

settings = LazySettings()

# rest_framework のRequest自動設定されているため


def get_user_jwt(request):
    user = None
    try:

        user_jwt = BaseTokenAuthentication().authenticate(Request(request))

        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except:
        pass

    return user or AuthUser()


class AuthenticateMiddleware(MiddlewareMixin):

    def process_request(self, request):
        pass
        #if request.content_type == "application/json":
            # request.auth_user = SimpleLazyObject(lambda: get_user_jwt(request))
            # 

            # request.role = get_role(request.user)
            # if not request.role:
            #     request.role = get_guest_role()