
from django.http import JsonResponse
from enum import Enum


class JsonResult():
    Success = '__success__'
    Failure = '__failure__'
    Error = '__error__'

class AmiJsonResopnse(JsonResponse):
    
    """
        
    """
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
