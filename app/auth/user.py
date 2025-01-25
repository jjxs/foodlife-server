import json
from app.base import JsonClass
import app.util as Util


class AuthUser(JsonClass):

    def __init__(self, json_str=None, init_data=None):
        self.result = ""
        self.message = ""
        self.data = ""
        self.language = ""
        self.authenticated = True
        self.user_id = ""
        self.user_account = ""
        self.user_name = ""
        self.options = {}
        self.authority = ""

        if json_str:
            print(json_str)
            dict_user = json.loads(json_str)
            Util.class_set_attrs(self, dict_user)

        if init_data:
            self.user_id = init_data['user_id']
            self.user_account = init_data['user_account']
            self.user_name = init_data['user_name']


    is_active = True

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return self.authenticated
