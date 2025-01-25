import json

class JsonClass(object):

    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
