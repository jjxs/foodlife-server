from django.db import models
from django.contrib.auth.models import User as SysUser
from django.contrib.postgres.fields import JSONField
from master.models.master import MasterData, MasterDataGroup
from master.models.guest import Guest
from django.db.models import Q
import common.const as Const


class SeatGroup(models.Model):
    # 席管理単位（部屋、エリアなど）

    no = models.CharField(max_length=20)

    name = models.CharField(max_length=200)
    start = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'seat_group'
        verbose_name = '座席グループ'
        verbose_name_plural = '座席グループ管理'

    def __str__(self):
        return str('%s %s' % (self.no, self.name))


class Seat(models.Model):
    # 席

    seat_no = models.CharField(max_length=20)

    name = models.CharField(max_length=200)

    start = models.DateTimeField(null=True, blank=True)  # 利用開始日

    # 利用できるかどうかを示す
    usable = models.NullBooleanField(null=True, blank=True)

    # 利用可能人数
    number = models.IntegerField(null=True, blank=True)

    # 席種別
    seat_type = models.ForeignKey(MasterData, related_name='seat_type', null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.seat_type})

    # 喫煙タイプ
    seat_smoke_type = models.ForeignKey(MasterData, related_name='seat_smoke_type', null=True, db_constraint=False,
                                        on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.seat_smoke_type})

    # 所属するGroup
    group = models.ForeignKey(SeatGroup, db_constraint=False, on_delete=models.DO_NOTHING)

    # 外卖坐席かどうかを示す
    takeout_type = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'seat'
        verbose_name = '座席'
        verbose_name_plural = '座席管理'

    def __str__(self):
        return str('%s %s' % (self.seat_no, self.name))


# class SeatCategory(models.Model):
#     # 座席分類
#     seat = models.ForeignKey(Seat,  db_constraint=False, on_delete=models.DO_NOTHING)
#     group = models.ForeignKey(MasterDataGroup, related_name='seat_category_group', null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'domain': 'SeatCategory'})
#     data = models.ForeignKey(MasterData, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

#     class Meta:
#         db_table = 'seat_category'
#         verbose_name = '座席分類'
#         verbose_name_plural = '座席分類'


class SeatStatus(models.Model):
    #　現時点のテーブル利用状況、利用中Seatのみ、スタッフによりデータ登録、会計後自動削除

    #　※※※※※食事途中で切り替え場合、注文の移転、合弁処理を必須（会計画面で）
    seat = models.ForeignKey(Seat,  db_constraint=False, on_delete=models.DO_NOTHING)

    # GUID TODO 毎回、利用開始後、counter_no作成し、注文はcounter_no単位でデータ登録
    counter_no = models.CharField(max_length=64)

    #　席利用者数(お通し追加必要あり)
    number = models.IntegerField(null=True, blank=True)

    #　利用開始 (TODO 一般で利用開始時間)
    start = models.DateTimeField(null=True, blank=True)

    #　利用終了時間
    end = models.DateTimeField(null=True, blank=True)

    # 簡易認証用GUID、毎度テーブル利用開始時作成、会計後終了、他人のテーブル利用防止、且つテーブル利用間違い防止、はじめて
    # 注文開始時点、サーバから取得、クライアント側保存、注文する際に検証で利用
    security_key = models.CharField(max_length=256)

    # 客類
    utype =  models.CharField(max_length=6)
    
    class Meta:
        db_table = 'seat_status'
        verbose_name = '座席利用状況'
        verbose_name_plural = '座席利用状況'

    def __str__(self):
        return str('%s ' % (self.seat.seat_no,))


# 現時点の座席利用者（デバイスで注文する方）


class SeatUser(models.Model):

    guest = models.ForeignKey(Guest, db_constraint=False, on_delete=models.DO_NOTHING)

    #　利用開始 (TODO 一般で利用開始時間)
    start = models.DateTimeField(null=True, blank=True)

    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'seat_user'


#　テーブル利用状況履历，会計後自動登録

class SeatStatusHistory(models.Model):
    seat = models.ForeignKey(Seat,  db_constraint=False, on_delete=models.DO_NOTHING)
    counter_no = models.CharField(max_length=64)    
    number = models.IntegerField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    security_key = models.CharField(max_length=256)

    class Meta:
        db_table = 'seat_status_history'


class SeatUserHistory(models.Model):
    guest = models.ForeignKey(Guest, db_constraint=False, on_delete=models.DO_NOTHING)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'seat_user_history'


class SeatFree(models.Model):
    seat = models.ForeignKey(Seat,  db_constraint=False, on_delete=models.DO_NOTHING)

    menu_free_id = models.IntegerField(null=True, blank=True)

    start = models.DateTimeField(null=True, blank=True)

    status = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'seat_free'

# class SeatHistory(models.Model):

#     Seat = models.ForeignKey(Seat, db_constraint=False, on_delete=models.DO_NOTHING)

#     tablename = models.CharField(max_length=32, null=True, blank=True)

#     history = JSONField()

#     creade = models.DateTimeField(auto_now_add=True, null=True, blank=True)

#     user = models.ForeignKey(SysUser, null=True, blank=True, db_constraint=False, on_delete=models.DO_NOTHING)

#     class Meta:
#         db_table = 'seat_history'
#         verbose_name = '座席履历'
#         verbose_name_plural = '座席履历'

#     def __str__(self):
#         return str('%s %s' % (self.sur_name, self.given_name))
