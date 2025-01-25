from django.db import models
from django.contrib.auth.models import User as SysUser
from django.contrib.postgres.fields import JSONField
from master.models.master import MasterData
from rest_framework.serializers import ModelSerializer


# バージョン1.0　簡易性を考慮の上、画面、Routerベースで制御
class Role(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    level = models.IntegerField(default=0)  # 　小さいほうレベル高い、複数権限持っているばあい、高い権限で利用する
    display_name = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'role'
        verbose_name = 'ロール'
        verbose_name_plural = 'ロール設定'

    def __str__(self):
        return str('%s' % (self.name))


class RoleDetail(models.Model):
    role = models.ForeignKey(Role, db_constraint=False, on_delete=models.DO_NOTHING)

    # => コメント理由：　
    # １、View単位で制御する、
    # ２、Rest設計 GET POST PUT DELETE単位で制御　
    # 　　登録	POST	CREATE
    # 　　取得	GET	　　READ
    # 　　更新	PUT	　　UPDATE
    # 　　削除	DELETE	DELETE
    # # TODO: ajaxアクセスする際に、サーバ側のチェック
    # allow_urls = JSONField()
    # deny_urls = JSONField()

    # # TODO: クライアント側制御用、画面は非正当手段で開いても、データ読み取りできないように、設計が必要
    # allow_router = JSONField()
    # deny_router = JSONField()

    VIEW_SELECTION = (
        ("guest.controller.guest.GuestController", "顧客関連情報"),
        ("guest.controller.guest.GuestDataController", "顧客情報"),
        ("guest.controller.guest.GuestDeviceController", "顧客設備情報"),
        ("restaurant.controller.seat.SeatController", "席情報"),
        ("master.controller.master.MasterController", "マスタ情報")
    )
    view = models.CharField(choices=VIEW_SELECTION, max_length=200, null=True, blank=True)

    ACTION_SELECTION = (
        ("ALLOW", "すべて"),
        ("POST", "登録"),
        ("GET", "取得"),
        ("PUT", "更新"),
        ("DELETE", "削除")
    )
    action = models.CharField(choices=ACTION_SELECTION, max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'role_detail'
        verbose_name = 'ロール詳細'
        verbose_name_plural = 'ロール詳細設定'

    def __str__(self):
        return str('%s=>%s' % (self.view, self.action))


class RoleUser(models.Model):
    user = models.ForeignKey(SysUser, db_constraint=False, on_delete=models.DO_NOTHING)
    role = models.ForeignKey(Role, db_constraint=False, on_delete=models.DO_NOTHING)
    note = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'role_user'
        verbose_name = 'ユーザロール設定'
        verbose_name_plural = 'ユーザロール設定'

    def __str__(self):
        return str('%s: %s' % (self.user, self.role))

