

from rest_framework.response import Response


class BusinessLogicException(Exception):

    def JsonResult(self):
        return Response({"error": "BusinessLogicException"})
