from django.db import models
from django.contrib.auth.models import User as SysUser
from django.contrib.postgres.fields import JSONField
from master.models.master import MasterData
from rest_framework.serializers import ModelSerializer

import common.const as Const

# TODO: 首次使用，通过扫码进入后，只要输入一个昵称，并且不重复就可以使用，生成Guest数据，
# TODO: 完善密码后，生成GuestUser用户


class Guest(models.Model):
    no = models.IntegerField(default=0, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    sur_name = models.CharField(max_length=100, null=True, blank=True)
    given_name = models.CharField(max_length=100, null=True, blank=True)
    sur_name_fricana = models.CharField(max_length=100, null=True, blank=True)
    given_name_fricana = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    sex = models.IntegerField(null=True, blank=True)
    tel = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    married = models.NullBooleanField(null=True, blank=True)
    final_education = models.ForeignKey(MasterData, blank=True, related_name='final_education', null=True, db_constraint=False, on_delete=models.DO_NOTHING,
                                        limit_choices_to={'group__name': Const.MasterGroup.final_education})
    created = models.DateTimeField(auto_now_add=True)
    is_temporary = models.NullBooleanField(null=True, blank=True)

    class Meta:
        db_table = 'guest'
        verbose_name = '顧客'
        verbose_name_plural = '顧客管理'

    def __str__(self):
        return str('%s %s' % (self.sur_name, self.given_name))


class GuestGroup(models.Model):
    # 管理上に便利のため
    name = models.CharField(max_length=200)
    evel = models.ForeignKey(MasterData, null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.geust_level})

    class Meta:
        db_table = 'guest_group'
        verbose_name = '顧客グループ'
        verbose_name_plural = '顧客グループ'

    def __str__(self):
        return str('%s' % (self.name))


class GuestGroupDetail(models.Model):
    # 管理上に便利のため
    guest = models.ForeignKey(Guest, db_constraint=False, on_delete=models.DO_NOTHING)
    guestgroup = models.ForeignKey(GuestGroup, db_constraint=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'guest_group_detail'
        verbose_name = '顧客グループ明細'
        verbose_name_plural = '顧客グループ明細'

    def __str__(self):
        return str('%s' % (self.name))


class GuestDevice(models.Model):
    guest = models.ForeignKey(Guest, related_name="devices", db_constraint=False, on_delete=models.DO_NOTHING)
    device_id = models.CharField(max_length=512)
    device_name = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.ForeignKey(MasterData, null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.device_type})
    note = models.CharField(max_length=1024, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guest_device'
        verbose_name = '利用モバイル管理'
        verbose_name_plural = '利用モバイル管理'


class GuestUser(models.Model):
    guest = models.ForeignKey(Guest, related_name="users", db_constraint=False, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(SysUser, db_constraint=False, on_delete=models.DO_NOTHING)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    # Loginしてない場合、Localstoreに保存、Loginする場合、同期する
    settings = JSONField()

    class Meta:
        db_table = 'guest_user'
        verbose_name = 'ログインユーザ関連'
        verbose_name_plural = 'ログイン関連'
