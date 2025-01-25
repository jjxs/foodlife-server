from common.util import Singleton
from master.data.system import SystemConfig
import math
from decimal import Decimal


class UtilTax(metaclass=Singleton):

    def tax(total, takeout=0):
        tax = SystemConfig.fax()
        if takeout:
            tax = SystemConfig.takeout_fax()
        return math.floor(Decimal(total) * (Decimal(1) + tax / Decimal(100)))

    def tax_value(total, takeout=0):
        # 税抜きから税金算出
        tax = SystemConfig.fax()
        if takeout:
            tax = SystemConfig.takeout_fax()
        total = Decimal(total)
        return math.floor(Decimal(total) * tax / Decimal(100))

    def tax_in(total, takeout=0):
        # 税込から税金算出
        tax = SystemConfig.fax()
        if takeout:
            tax = SystemConfig.takeout_fax()
        value = math.floor(Decimal(total) / (Decimal(1) + tax / Decimal(100)))
        return UtilTax.tax_value(value, takeout)

    def tax_in_value(total, takeout=0):
        # 税込から税抜き算出
        tax = UtilTax.tax_in(total, takeout)
        return total - tax
