from master.models.master import MasterData, Config
import common.const as Const
from decimal import *


class SystemConfig(object):
    __master = None
    __system_name = ""
    __fax = 10
    __takeout_fax = 8
    __shop_info = {}
    __version = ""
    __whitelist = []
    __qrtheme = ""

    @classmethod
    def create(cls):
        masters = MasterData.objects.filter(group__name=Const.MasterGroup.system_config)
        for master in masters:
            if master.name == "system_name":
                cls.__system_name = master.extend

            elif master.name == "fax":
                cls.__fax = Decimal(master.extend)
            
            elif master.name == "takeout_fax":
                cls.__takeout_fax = Decimal(master.extend)

            elif master.name == "shop_info":
                cls.__shop_info = master.option

            elif master.name == "version":
                cls.__version = master.extend
            
            elif master.name == "whitelist":
                cls.__whitelist = master.extend

            elif master.name == "qrtheme":
                cls.__qrtheme = master.extend

    @classmethod
    def system_name(cls):
        if cls.__master is None:
            cls.create()
        configs = Config.objects.filter(key='shopinfo')
        if len(configs)>0:
            config = configs[0]
            if 'name' in config.value:
                cls.__system_name = config.value['name']
        return cls.__system_name

    @classmethod
    def fax(cls):
        if cls.__master is None:
            cls.create()

        return cls.__fax
    
    @classmethod
    def takeout_fax(cls):
        if cls.__master is None:
            cls.create()

        return cls.__takeout_fax

    
    @classmethod
    def qrtheme(cls):
        if cls.__master is None:
            cls.create()

        return cls.__qrtheme
    
    @classmethod
    def shop_info(cls):
        if cls.__master is None:
            cls.create()

        return cls.__shop_info

    @classmethod
    def version(cls):
        if cls.__master is None:
            cls.create()

        return cls.__version

    @classmethod
    def whitelist(cls, addr):
        if cls.__whitelist is None:
            cls.create()
        
        configs = Config.objects.filter(key='whitelist')
        if len(configs)>0:
            config = configs[0]
            cls.__whitelist = config.value
        
        if not cls.__whitelist or addr in cls.__whitelist:
            return True
        else:
            return False
