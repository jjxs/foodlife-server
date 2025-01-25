
import math
from decimal import Decimal


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class UtilTax(metaclass=Singleton):

    def tax(total):
        tax = Decimal(8)
        return math.floor(Decimal(total) * (Decimal(1) + tax / Decimal(100)))

    def tax_value(total):
        # 税抜きから税金算出
        tax = Decimal(8)
        total = Decimal(total)
        return math.floor(Decimal(total) * tax / Decimal(100))

    def tax_in(total):
        # 税込から税金算出
        tax = Decimal(8)
        value = math.floor(Decimal(total) / (Decimal(1) + tax / Decimal(100)))
        return UtilTax.tax_value(value)

    def tax_in_value(total):
        # 税込から税抜き算出
        tax = UtilTax.tax_in(total)
        return total - tax


for i in range(20000):
    value = UtilTax.tax_in_value(i)
    tax = UtilTax.tax_in(i)
    print('{0} = {1} + {2} {3}'.format(i, value, tax, i == value + tax))
