from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class MasterDataGroup(models.Model):
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=100, null=True, blank=True)

    # 利用区分（管理上に簡易のため）
    domain = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)

    display_order = models.IntegerField(default=0, null=True, blank=True)
    extend = models.CharField(max_length=1024, null=True, blank=True)
    option = JSONField(null=True, blank=True)
    enabled = models.IntegerField(default=1)

    class Meta:
        db_table = 'master_data_group'
        verbose_name = 'マスタデータグループ管理'
        verbose_name_plural = 'マスタデータグループ'

    def __str__(self):
        return str('%s: %s' % (self.id, self.display_name))


class MasterData(models.Model):
    group = models.ForeignKey(MasterDataGroup, related_name='master_data', db_constraint=False, on_delete=models.DO_NOTHING)
    code = models.IntegerField(default=0)
    name = models.CharField(max_length=500)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    display_order = models.IntegerField(default=0, null=True, blank=True)
    theme_id = models.CharField(max_length=50, null=True, blank=True)
    menu_count = models.IntegerField(default=0, null=True, blank=True)
    note = models.CharField(max_length=1024, null=True, blank=True)
    extend = models.CharField(max_length=1024, null=True, blank=True)
    option = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'master_data'
        ordering = ('display_order',)
        verbose_name = 'マスタデータ管理'
        verbose_name_plural = 'マスタデータ'

    def __str__(self):
        return str('%s: (%s:%s)' % (self.group, self.id, self.name))


# TODO　多国語利用しない場合、nameはそのまま利用、多国語利用する場合、対象nameは識別IDとして、利用する
# TODO　Languageデータをキャッシュして、取得用AIP提供
class Language(models.Model):

    # 多国語利用するテーブルで定義した識別ID
    name = models.CharField(max_length=200, null=True, blank=True)

    # TODO HTMLデータ管理用　識別名称(クライアント側と連携する際に)
    html_name = models.CharField(max_length=200, null=True, blank=True)

    ja = models.CharField(max_length=200, null=True, blank=True)
    en = models.CharField(max_length=200, null=True, blank=True)
    zh = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = '言語データ'
        verbose_name_plural = '言語データ'


class Config(models.Model):
    # 任意保存したい設定情報
    # TODO 共通メソッドにより利用

    # 例えば為替レートは開店時、最新のレートを取得し、設定
    key = models.CharField(max_length=200, null=True, blank=True)
    value = JSONField()

    # 例　user_language: ['ja','zh','kr','en']
    # 　  exchagne_rate: {
    #        'ja': 0.004,
    #        'zh': 0.004,
    #        'kr': 0.004,
    #        'en': 0.004,
    #     }

    class Meta:
        verbose_name = '設定'
        verbose_name_plural = '設定'


class MstReport(models.Model):
    # 任意保存したい設定情報
    # TODO 共通メソッドにより利用

    # 例えば為替レートは開店時、最新のレートを取得し、設定
    report_type = models.CharField(max_length=20, null=True, blank=True)
    report_date = models.CharField(max_length=10, null=True, blank=True)
    report = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'mst_report'


class MstReportHistory(models.Model):
    # 任意保存したい設定情報
    # TODO 共通メソッドにより利用

    # 例えば為替レートは開店時、最新のレートを取得し、設定
    report_type = models.CharField(max_length=20, null=True, blank=True)
    report_date = models.CharField(max_length=10, null=True, blank=True)
    report = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'mst_report_history'
