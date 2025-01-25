
from django.conf import settings
from sqlalchemy.pool import manage
import time

POOL_SETTINGS = {}
POOL_SETTINGS.setdefault("recycle", 0)


class SaasHandler():

    __saas_id = ""
    __setting = {}
    __detail = {}
    __plugin = []
    __status = False

    @classmethod
    def set_saas_id(cls, saas_id):
        # params = request.GET
        # if '__SAAS_ID__' in params:
        #     saas_id = params['__SAAS_ID__']
        #     if saas_id!="null":
        cls.__saas_id = saas_id
    
    @classmethod
    def get_saas_id(cls):
        if cls.__saas_id!="" and cls.__saas_id!="default" and cls.__saas_id!="undefined":
            return cls.__saas_id
        else:
            return ""

    @classmethod
    def set_status(cls, status):
        cls.__status = status

    @classmethod
    def get_status(cls):
        return cls.__status
    
    @classmethod
    def set_setting(cls, setting):
        cls.__setting = setting
        
    @classmethod
    def get_setting(cls):
        return cls.__setting
        
    @classmethod
    def get_db(cls):
        result = {}
        if cls.__setting!={}:
            result['database'] = cls.__setting['db_name']
            result['user'] = cls.__setting['db_user']
            result['password'] = cls.__setting['db_pwd']
            result['host'] = cls.__setting['db_host']
            result['port'] = cls.__setting['db_port']
        return result

    @classmethod
    def get_cache(cls):
        result = {}
        if cls.__setting!={}:
            result['namespace'] = cls.__setting['cache_namespace']
            result['host'] = cls.__setting['cache_host']
            result['port'] = cls.__setting['cache_port']
        return result

    @classmethod
    def get_s3(cls):
        result = {}
        if cls.__setting!={}:
            result['namespace'] = cls.__setting['s3_namespace']
        return result

    
    @classmethod
    def set_plugin(cls, plugins):
        cls.__plugin = plugins

        
    @classmethod
    def get_plugin(cls):
        return cls.__plugin
    
    @classmethod
    def set_shopDetail(cls, detail):
        cls.__detail = detail
    
    @classmethod
    def get_shopDetail(cls):
        return cls.__detail


def is_iterable(value):
    """Check if value is iterable."""
    try:
        _ = iter(value)
        return True
    except TypeError:
        return False


class HashableDict(dict):
    def __hash__(self):
        items = [(n, tuple(v)) for n, v in self.items() if is_iterable(v)]
        return hash(tuple(items))


class ManagerProxy(object):
    __db_cache = {}
    def __init__(self, manager):
        self.manager = manager

    def __getattr__(self, key):
        return getattr(self.manager, key)

    def connect(self, *args, **kwargs):
        # saas 
        saas_id = SaasHandler.get_saas_id()
        if saas_id!="":
            print("ID:{0} HOST: {1}:{2} DB:{3} {4} {5}".format(saas_id, kwargs['host'], kwargs['port'], kwargs['database'], "--------------get saas info--------", time.time()))
            if self.__db_cache == {}:
                saas_db = {
                    'database': settings.DATABASES["saas-manage"]['NAME'],
                    'user': settings.DATABASES["saas-manage"]['USER'],
                    'password': settings.DATABASES["saas-manage"]['PASSWORD'],
                    'host': settings.DATABASES["saas-manage"]['HOST'],
                    'port': settings.DATABASES["saas-manage"]['PORT']
                }
                saas_conn = self.manager.connect(*{}, **saas_db)
                exe_sql = "SELECT shop_setting.* FROM shop_setting INNER JOIN shop ON shop.saas_id = shop_setting.saas_id WHERE shop_setting.saas_id = %(saas_id)s AND shop.shop_status=1 limit 1"
                params = {}
                params["saas_id"] = saas_id
                with saas_conn.cursor() as cursor:
                    # cursor.execute("ALTER SESSION SET NLS_TERRITORY = 'JAPAN' ")
                    cursor.execute(exe_sql, params)
                    columns = [col[0] for col in cursor.description]
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

                    if len(rows):
                        shop_setting = rows[0]
                        SaasHandler.set_setting(shop_setting)
                        SaasHandler.set_status(True)
                    else:
                        SaasHandler.set_saas_id("")
                        SaasHandler.set_status(False)
                        raise Exception("db error")
                    
                    exe_sql = "SELECT plugin_name FROM shop_plugin WHERE saas_id = %(saas_id)s AND plugin_status=1"
                    cursor.execute(exe_sql, params)
                    columns = [col[0] for col in cursor.description]
                    plugin = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    SaasHandler.set_plugin(plugin)

                    exe_sql = "SELECT shop_name, shop_tel, saas_id FROM shop WHERE saas_id = %(saas_id)s"
                    cursor.execute(exe_sql, params)
                    columns = [col[0] for col in cursor.description]
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    SaasHandler.set_shopDetail(rows[0])

            kwargs = SaasHandler.get_db()
            args = {}
            print("ID:{0} HOST: {1}:{2} DB:{3} {4} {5}".format(saas_id, kwargs['host'], kwargs['port'], kwargs['database'], "--------------get saas info ok--------", time.time()))

        if 'conv' in kwargs:
            kwargs['conv'] = HashableDict(kwargs['conv'])

        if 'ssl' in kwargs:
            kwargs['ssl'] = HashableDict(kwargs['ssl'])

        return self.manager.connect(*args, **kwargs)


def patch_pgsql():
    from django.db.backends.postgresql import base as pgsql_base

    if not hasattr(pgsql_base, "_Database"):
        pgsql_base._Database = pgsql_base.Database
        manager = manage(pgsql_base._Database, **POOL_SETTINGS)
        pgsql_base.Database = ManagerProxy(manager)




def install_patch():
    patch_pgsql()