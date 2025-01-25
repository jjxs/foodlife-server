
from django_filters import rest_framework as filters

# /master/masterdata/?group__name__in=seat_type,seat_smoke_type
class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass
