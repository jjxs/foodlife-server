
from rest_framework.response import Response


class WebLogicException(Exception):

    def __init__(self, message):
        self.message = message

    def JsonResult(self):
        return {"error": self.message}
