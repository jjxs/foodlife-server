from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from common.exception.business import BusinessLogicException
from common.exception.web import WebLogicException
from common.log import logger
from django.http import JsonResponse
from rest_framework.decorators import api_view
import traceback


class ExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):

        print("*************** process_exception ****************")
        #logger.info("ERROR: " + exception)
        print("TRACEBACK: " + traceback.format_exc())
        result = {"error": str(exception), "status": 500}
        


        if isinstance(exception, BusinessLogicException):
            result = exception.JsonResult()

        if isinstance(exception, WebLogicException):
            result = exception.JsonResult()

        return JsonResponse(result)  # Response({"error": "ExceptionMiddleware"})
