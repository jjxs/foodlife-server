from datetime import datetime, date
from django.forms.models import model_to_dict
import json


def support_datetime_default(o):
    if isinstance(o, date):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Util(metaclass=Singleton):

    def current_string(format="%Y/%m/%d %H:%M:%S.%f"):
        now = datetime.now()
        return now.strftime(format)

    def current():
        return datetime.now()

    def model_to_dict(model):
        return model_to_dict(model)

    def model_to_json(model):
        '''
        Django model => dict => json string
        '''
        dc = model_to_dict(model)
        js = json.dumps(dc, default=support_datetime_default)
        return js

    def encode(obj):
        data = json.dumps(obj, default=support_datetime_default)
        return data

    def is_empty(obj):
        if obj == None:
            return True

        if isinstance(obj, str) and not obj:
            return True
        
        return True;
