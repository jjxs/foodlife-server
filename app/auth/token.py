from calendar import timegm
from datetime import datetime
import warnings
import uuid
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field
import jwt

from django.contrib.auth import get_user_model
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


import json
from app.auth.user import AuthUser
import time
from app.db.db_patch import SaasHandler

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class BaseTokenAuthentication(JSONWebTokenAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        print("*************** get_user_jwt authenticate 0 ****************")

        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        json_user = payload.get('user')

        return (AuthUser(json_user), jwt_value)


def jwt_payload_handler(user):
    ''' JWT 作成する場合、これを呼ばれます '''

    # username_field = get_username_field()
    # username = get_username(user)

    # warnings.warn(
    #     'The following fields will be removed in the future: '
    #     '`email` and `user_id`. ',
    #     DeprecationWarning
    # )

    payload =  {
        'user_id': user.id,
        'username': user.username,
        'exp': int(time.time()) + 86400000,
        'email': user.email,
        'saas_id': SaasHandler.get_saas_id()
    }

    return payload


# def jwt_response_payload_handler(token, user=None, request=None):
#     """
#     Returns the response data for both the login and refresh views.
#     Override to return a custom response such as including the
#     serialized representation of the User.

#     Example:

#     def jwt_response_payload_handler(token, user=None, request=None):
#         return {
#             'token': token,
#             'user': UserSerializer(user, context={'request': request}).data
#         }

#     """
#     print("------------------- jwt_response_payload_handler --------------------")
#     print(user)

#     return {
#         'token': token,
#         'auth_user': AuthUser()
#     }
