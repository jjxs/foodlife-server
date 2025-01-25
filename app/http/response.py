

from rest_framework.response import Response


class JsonResult(object):

    def __init__(self, data="", result=True, message="Success", errors={}):
        self.result = result
        self.message = message
        self.data = data
        self.errors = errors

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        yield 'result', self.result
        yield 'message', self.message
        yield 'data', self.data
        yield 'errors', self.errors

    # def __iter__(self):
    #     return self

    def keys(self):
        return ['result', 'message', 'data', 'errors']

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


class JsonResponse(Response):

    def __init__(self, data="", result=True, message="Success", errors={}):

        super(JsonResponse, self).__init__(data=JsonResult(
            data=data, result=result, message=message, errors=errors))
