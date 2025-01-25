
from rest_framework.utils.encoders import JSONEncoder
import json
from datetime import datetime, date



class JsonResult(object):

    # def default(self, o):
    #     return {
    #         'result': o.result,
    #         'message': o.message,
    #         'data': o.data
    #     }

    def __init__(self, data="", result=True, message="Success"):
        self.result = result
        self.message = message
        self.data = data

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        yield 'result', self.result
        yield 'message', self.message
        yield 'data', self.data

    # def __iter__(self):
    #     return self

    def keys(self):
        return ['result', 'message', 'data']

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
