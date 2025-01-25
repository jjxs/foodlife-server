from django.db import models
from django.contrib.auth.models import User as SysUser
from django.contrib.postgres.fields import JSONField
from master.models.master import MasterData,  MasterDataGroup
from master.models.guest import Guest
import common.const as Const
# 料理分類


class Menu(models.Model):

    no = models.IntegerField(default=0)

    # 言語ID ＝＞ 多国語取得用
    name = models.CharField(max_length=200, null=True, blank=True)

    #　在庫状況など
    stock_status = models.ForeignKey(MasterData, null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.menu_stock_status})

    # 注文できるかどうかを示す（在庫ない場合利用不可にする）
    usable = models.BooleanField()

    # 原始金額（主な利用通貨で、他国通貨への為替はConfifで定義した為替で決まる）
    ori_price = models.DecimalField(max_digits=8, decimal_places=0)
    
    # 金額（主な利用通貨で、他国通貨への為替はConfifで定義した為替で決まる）
    price = models.DecimalField(max_digits=8, decimal_places=0)
    
    # 税込であるかどうか
    tax_in = models.BooleanField(default=False)
    
    # プロパティ
    note = models.CharField(max_length=200, null=True, blank=True)

    # 説明文
    introduction = models.TextField(null=True, blank=True)

    
    # photo
    image = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'menu'
        verbose_name = '料理'
        verbose_name_plural = '料理データ'

    def __str__(self):
        return str('%s:%s' % (self.name, self.no))


class MenuCategory(models.Model):
    # 料理分類

    # 分類グループ（ 標準分類、国別、エリア、味、价格区间）
    # 分類グループの明細＝＞メニュー画面Tabに表示
    category = models.ForeignKey(MasterData, related_name='category', null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    menu = models.ForeignKey(Menu, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    # 分類内の表示順
    display_order = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        db_table = 'menu_category'
        verbose_name = '料理'
        verbose_name_plural = '料理区分'

    def __str__(self):
        return str('%s %s' % (self.category, self.menu))


class MenuOption(models.Model):
    # 料理注文時選択可能オプション(辛さなお)

    data = models.ForeignKey(MasterData, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    menu = models.ForeignKey(Menu, db_constraint=False, on_delete=models.DO_NOTHING)
    #　icon name(画面表示用)
    icon = models.CharField(max_length=200, null=True, blank=True)

    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu_option'
        verbose_name = '料理選オプション'
        verbose_name_plural = '料理選択可能のオプション'


class MenuCourse(models.Model):
    # コース料理定義
    # TODO コース注文後、該当テーブルで定義したメニューでまとめて注文
    # TODO 順番あることを要注意

    # 管理用メニュー（割引、注文用）
    menu = models.ForeignKey(Menu, db_constraint=False, on_delete=models.DO_NOTHING, null=True)

    # 言語ID ＝＞ 多国語取得用
    name = models.CharField(max_length=200, null=True, blank=True)

    # 金額（主な利用通貨で、他国通貨への為替はConfifで定義した為替で決まる）
    price = models.DecimalField(max_digits=8, decimal_places=0)

    # 税込であるかどうか
    tax_in = models.BooleanField(default=False)

    # 料理の優先順位
    level = models.IntegerField(default=0)

    # 数量
    count = models.IntegerField(default=0)

    # 料理あげる順番
    display_order = models.IntegerField(default=0)

    #　利用可能時間、0の場合制限無し（食べ放題などで利用する）
    usable_time = models.IntegerField(default=0)

    # 取消可能時間
    cancel_possible = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu_course'


class MenuCourseDetail(models.Model):
    # コース料理明細
    menu_course = models.ForeignKey(MenuCourse, null=True, db_constraint=False, on_delete=models.DO_NOTHING)
    menu = models.ForeignKey(Menu, null=True, db_constraint=False, on_delete=models.DO_NOTHING)
    group_id = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu_course_detail'


class MenuFree(models.Model):
    # 食べ放
    # L、飲み放題定義
    # TODO 放題注文後、「放題メニュー」利用可能にする、
    # TODO ☆放題メニュー以外のメニューは、放題対象商品の金額を 「放題」で表示する

    # 管理用メニュー（割引、注文用）1対1
    menu = models.ForeignKey(Menu, related_name='menu_free', db_constraint=False, on_delete=models.DO_NOTHING, null=True)

    # 食べ放題、飲み放題、食べ飲み放題
    free_type = models.ForeignKey(MasterData, related_name='free_type', null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.free_type})

    # 言語ID ＝＞ 多国語取得用
    name = models.CharField(max_length=200, null=True, blank=True)

    #　利用可能時間、0の場合制限無し（食べ放題などで利用する）
    usable_time = models.IntegerField(default=0)

    #　表示順
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu_free'
        verbose_name = '放題メニュー設定'
        verbose_name_plural = '放題メニュー設定'

    def __str__(self):
        return str('%s' % (self.menu))


class MenuFreeDetail(models.Model):

    # 食べ放題、飲み放題定義明細
    menu_free = models.ForeignKey(MenuFree, related_name='menus', null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    menu = models.ForeignKey(Menu, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'menu_free_detail'
        verbose_name = '放題メニュー'
        verbose_name_plural = '放題メニュー'


# class DrinkFree(models.Model):
#     # 食べ放題、飲み放題定義
#     # TODO 放題注文後、「放題メニュー」利用可能にする、
#     # TODO ☆放題メニュー以外のメニューは、放題対象商品の金額を 「放題」で表示する

#     # 管理用メニュー（割引、注文用）
#     menu = models.ForeignKey(Menu, db_constraint=False, on_delete=models.DO_NOTHING, null=True)

#     # 言語ID ＝＞ 多国語取得用
#     name = models.CharField(max_length=200, null=True, blank=True)

#     #　表示順
#     usable_time = models.IntegerField(default=0)

#     # 料理あげる順番
#     display_order = models.IntegerField(default=0)

#     class Meta:
#         db_table = 'drink_free'
#         verbose_name = '飲み放題メニュー設定'
#         verbose_name_plural = '飲み放題メニュー設定'

#     def __str__(self):
#         return str('%s' % (self.menu))


# class DrinkFreeDetail(models.Model):

#     # 食べ放題、飲み放題定義明細
#     drink_free = models.ForeignKey(DrinkFree, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

#     menu = models.ForeignKey(Menu, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

#     class Meta:
#         db_table = 'drink_free_detail'
#         verbose_name = '飲み放題メニュー'
#         verbose_name_plural = '飲み放題メニュー'


class MenuSale(models.Model):
    '''
    メニュー価格
    '''
    menu = models.ForeignKey(Menu, db_constraint=False, on_delete=models.DO_NOTHING)

    # TODO　is_allで定義した場合、全品可能
    is_all = models.NullBooleanField(null=True, blank=True)

    # TODO　価格
    price = models.DecimalField(max_digits=8, decimal_places=0)

    # TODO　比率
    ratio = models.DecimalField(max_digits=8, decimal_places=2)

    # 無限期
    is_infinite = models.NullBooleanField(null=True, blank=True)

    # 利用開始期間(TODO 重複する場合、安いほうで決まる)
    start = models.DateTimeField(null=True)

    # 利用終了期間
    end = models.DateTimeField(null=True)

    # 注文可能数
    # TODO 一人分、テーブルの人数分注文可能
    max_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu_sale'


class MenuComment(models.Model):
    # メニュー評判

    guest = models.ForeignKey(Guest, db_constraint=False, on_delete=models.DO_NOTHING)

    menu = models.ForeignKey(Menu, db_constraint=False, on_delete=models.DO_NOTHING)

    # good or bed
    good = models.NullBooleanField()

    # 評判
    comment = models.TextField()

    # 登録時間
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'menu_comment'



class MenuTop(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    target_type = models.CharField(max_length=20, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=True)
    sort = models.IntegerField(default=0, null=True, blank=True)
    option = models.TextField(default='', null=True, blank=True)
    enabled = models.IntegerField(default=0, null=True, blank=True)
    menu_type = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'menu_top'
        verbose_name = 'menu top 管理'
        verbose_name_plural = 'menu top '

class MenuBind(models.Model):
    menu_id = models.IntegerField(default=0, primary_key=True)
    bind_id = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu_bind'
        verbose_name = 'menu bind 管理'
        verbose_name_plural = 'menu bind '

class MenuGift(models.Model):

    menu_id = models.IntegerField(null=True, blank=True)

    use_gift_count = models.IntegerField(null=True, blank=True)

    flg = models.BooleanField(default=False)

    class Meta:
        db_table = 'menu_gift'
