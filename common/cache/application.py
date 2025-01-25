class Application(object):
    __count = 0 

    @classmethod
    def get_count(cls):
        return cls.__count

    @classmethod
    def set_count(cls, num):
        cls.__count = num
