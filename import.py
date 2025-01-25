from master.models.seat import *
from common.util import Util
from datetime import datetime as dt


#!/usr/bin/env python
import os
import sys
import django.core.set

settings.configure()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
try:
    from django.core.management import execute_from_command_line
except ImportError:
    # The above import may fail for some other reason. Ensure that the
    # issue is really that Django is missing to avoid masking other
    # exceptions on Python 2.
    try:
        import django
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    raise


def seat():
    rows = [

    ]
    for row in rows:
        print(row)
        dt = dt.strptime(row.start, '%Y-%m-%d %H:%M:%S')
        seat_type = MasterData.objects.get(id=row.seat_type_id)
        seat_smoke_type = MasterData.objects.get(id=row.seat_smoke_type_id)
        group = SeatGroup.objcts.get(id=row.group_id)
        Seat.objects.create(
            id=row.id,
            seat_no=row.seat_no,
            name=row.name,
            start=dt,
            usable=row.usable,
            number=row.number,
            seat_type=seat_type,
            seat_smoke_type=seat_smoke_type,
            group=group)


def seat_group():

    rows = [
        (1, 1001, '左エリア'),
        (2, 1002, '右エリア'),
        (3, 1003, '個室'),
        (4, 1004, '外食')
    ]
    now = Util.current()
    for row in rows:
        id, no, name = row
        SeatGroup.objects.create(
            id=id,
            no=no,
            name=name,
            start=now
        )


seat()
