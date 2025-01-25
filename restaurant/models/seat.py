from django.db import models
from rest_framework import serializers

# DB Table存在しない、単純データ通信用クラス


class SeatList(models.Model):
    seat_no = models.CharField(max_length=100)

    name = models.CharField(max_length=100)

    # 設置開始時間
    start = models.DateTimeField(null=True, blank=True)

    # 利用できるかどうかを示す
    usable = models.NullBooleanField(null=True, blank=True)

    # 利用可能人数
    number = models.IntegerField(null=True, blank=True)

    # 席種別
    seat_type = models.CharField(max_length=100)

    # 喫煙タイプ
    seat_smoke_type = models.CharField(max_length=100)

    # 所属するGroup group_no
    group_no = models.CharField(max_length=100)

    # 所属するGroup group_name
    group_name = models.CharField(max_length=100)

    # 利用開始時間
    use_start = models.DateTimeField(null=True, blank=True)

    # 利用人数
    guest_number = models.IntegerField(null=True, blank=True)

    # 客類
    guest_utype = models.CharField(max_length=6)


class SeatCondition(object):
    def __init__(self):

        self.seat_group = list()
        self.seat_type = list()
        self.seat_smoke_type = list()
        self.seat_number = list()
        self.seat_usable = ""
