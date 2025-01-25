from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from rest_framework.decorators import api_view
import traceback
from django.http import HttpResponseServerError

from app.http.response import JsonResponse
import app.log.logger as Logger
from app.exception.web import WebException


class ExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):

        if isinstance(exception, WebException):

            # result = exception.to_json()
            error = str(exception)
        else:
            error = "システムエラーです。管理者へご連絡してください。! "

        Logger.error(error + "\n  TRACEBACK: " + traceback.format_exc())

        # return JsonResponse(result=True, data=result)  # Response({"error": "ExceptionMiddleware"})
        return HttpResponseServerError(error)
