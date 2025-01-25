from rest_framework.response import Response
import app.common.message as Message


class WebException(Exception):

    def __init__(self, message_id=None, message=None, language="J"):

        if message_id:
            self.message = Message.get_by_id(message_id)
        else:
            self.message = message

    def __str__(self):
        return self.message

    # def to_json(self):
    #     return {"error": self.message, "status": 500}
