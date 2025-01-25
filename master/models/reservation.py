from django.db import models
from django.contrib.auth.models import User as SysUser
from django.contrib.postgres.fields import JSONField
from master.models.menu import Menu, MenuCourse, MenuFree
from master.models.guest import Guest
from master.models.seat import Seat
from master.models.master import MasterData, MasterDataGroup
from master.models.order import Order, OrderDetail
import common.const as Const


class Reservation(models.Model):

    #　予約NO管理用
    reservation_no = models.CharField(max_length=64)

    # 来店予約、持ち帰り予約
    Reservation_type = models.ForeignKey(MasterData, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.reservation_type})

    name = models.CharField(max_length=100, null=True, blank=True)

    tel = models.CharField(max_length=30, null=True, blank=True)

    phone = models.CharField(max_length=30, null=True, blank=True)

    # 予約来店時間
    reservation_time = models.DateTimeField(null=True, blank=True)

    # 利用人数
    number = models.IntegerField(null=True, blank=True)

    #　ある場合（自ら予約する場合）
    guest = models.ForeignKey(Guest, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    # 来店後作成し、ここに登録　
    counter_no = models.CharField(max_length=64)

    # 来店時間
    enter_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'reservation'
        verbose_name = '予約管理'
        verbose_name_plural = '予約管理'

    def __str__(self):
        return str('%s=>%s:%s' % (self.reservation_no, self.reservation_time, self.name))


class ReservationSeat(models.Model):

    reservation = models.ForeignKey(Reservation, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    Seat = models.ForeignKey(Seat,  db_constraint=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'reservation_detail'


class ReservationMenu(models.Model):

    reservation = models.ForeignKey(Reservation, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    menu = models.ForeignKey(Menu, null=True, db_constraint=False, on_delete=models.DO_NOTHING)
    menu = models.ForeignKey(MenuCourse, null=True, db_constraint=False, on_delete=models.DO_NOTHING)
    menu = models.ForeignKey(MenuFree, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'reservation_menu'


class ReservationHistory(models.Model):
    # 閉店処理際に、当日予約ずみ内容を履歴へ登録

    reservation_no = models.CharField(max_length=64)

    Reservation = JSONField()
    ReservationDetail = JSONField()

    class Meta:
        db_table = 'reservation_history'
