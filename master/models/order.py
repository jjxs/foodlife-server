from django.db import models
from django.contrib.auth.models import User as SysUser
from django.contrib.postgres.fields import JSONField

from master.models.menu import Menu, MenuFree
from master.models.guest import Guest
from master.models.seat import Seat
from master.models.master import MasterData, MasterDataGroup
import common.const as Const

# 利用中の注文データ、閉店後注文履歴へ移動


class Takeout(models.Model):
    #　持ち帰り
    # TODO 持ち帰り画面から、開始を入力し　＝＞　メニュー画面へ遷移（持ち帰りカテゴリーで定義したメニューのみ画面へ表示）

    # GUID TODO 毎回、利用開始後、counter_no作成し、注文はcounter_no単位でデータ登録
    counter_no = models.CharField(max_length=64)

    class Meta:
        db_table = 'takeout'


class Order(models.Model):

    # 管理用 オーダー番号20180910154448649805
    order_no = models.CharField(max_length=20)  # 9999123100000001

    counter_no = models.CharField(max_length=64)

    seat = models.ForeignKey(Seat, null=True, related_name='order_seat', db_constraint=False, on_delete=models.DO_NOTHING)

    # #　確認済みである、食べ放題、コース料理は、確認済みでないと、すすまない
    # order_confirm = models.NullBooleanField(null=True, blank=True, default=True)

    # 注文タイプ (店内、店外) 　
    # 注文する確認する場合、選択
    # TODO ※メニュー画面は持ち帰りモードで開く場合、店外のみ選択できます。
    order_type = models.ForeignKey(MasterData, null=True, blank=True, related_name='order_type', db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.order_type})

    # 注文手段（ユーザロールにより手段を判明、TODO ※ログイン,ロールから注文手段を特定する）
    # 1: 管理ロール
    # 　　テーブル選択＝＞注文（会計、管理者など） （ユーザ認証のみ、テーブル切り替え可能）
    #    ＝＞ ログイン後、設定画面で選択する（Localstoreに保存する、毎回設定不要）
    #
    # 2: 店員ロール　注文（店員持ちデバイス）　
    # 　　テーブル選択＝＞注文（店員など）（ユーザ認証のみ、テーブル切り替え可能）
    #    ＝＞ ログイン後、設定画面で選択する（Localstoreに保存する、毎回設定不要）
    #
    # 3: 顧客ロール　携帯
    # 　　スキャンしてsecurity_key取得して利用、テーブル切り替えはスキャンが必要
    #    ＝＞ スキャンによりログイン後、自動設定、
    #         またはgeustユーザでログイン後 ※顧客デバイス情報＝＞GuestDeviceに吸収
    #
    # 4: 注文専用PAD
    # 　　特別ロールがあるUSERで認証し、利用可能
    # 　　　　　　　　　　　切り替え不可にする（切り替え可能ユーザで認証し、切り替え後特別ロールに戻る）
    #    ＝＞ 特別ロールにログイン後
    order_method = models.ForeignKey(MasterData, null=True, blank=True, related_name='order_method', db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.order_method})

    # 存在する場合
    guest = models.ForeignKey(Guest, db_constraint=False, on_delete=models.DO_NOTHING, blank=True, null=True)

    # 存在する場合（店員さん、管理者の場合）
    user = models.ForeignKey(SysUser, db_constraint=False, on_delete=models.DO_NOTHING, blank=True, null=True)

    order_time = models.DateTimeField(auto_now_add=True)

    ship_addr = models.CharField(max_length=200, blank=True, null=True)
    ship_name = models.CharField(max_length=50, blank=True, null=True)
    ship_tel = models.CharField(max_length=32, blank=True, null=True)
    ship_time = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = 'order'
        verbose_name = '注文'
        verbose_name_plural = '注文データ'

    def __str__(self):
        return str('%s %s' % (self.order_no, self.counter_no))

# 注文明細


class OrderDetail(models.Model):

    order = models.ForeignKey(Order, related_name='order_detail', db_constraint=False, on_delete=models.DO_NOTHING)

    # 注文内容
    menu = models.ForeignKey(Menu, related_name='order_detail_menu', db_constraint=False, on_delete=models.DO_NOTHING)

    # 金額（主な利用通貨で、他国通貨への為替はConfifで定義した為替で決まる）注文時金額を決まります
    price = models.DecimalField(max_digits=8, decimal_places=0)

    # 原始金額（主な利用通貨で、他国通貨への為替はConfifで定義した為替で決まる）
    ori_price = models.DecimalField(max_digits=8, decimal_places=0)

    # TODO　オプション選択可能メニュー注文する際に、指定できます。
    menu_option = JSONField(null=True, blank=True)

    # TODO　オプション選択可能メニュー注文する際に、指定できます。
    option = JSONField(null=True, blank=True)

    # 数量
    count = models.IntegerField(default=0)

    #　取消可能かどうか
    cancelable = models.NullBooleanField()

    # # マスターデータ、現在のステータス(現在の処理状況)　作成中に変更したら、取り消し不可にする
    # status = models.ForeignKey(MasterData, null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.order_detail_status})

    class Meta:
        db_table = 'order_detail'
        verbose_name = '注文明細'
        verbose_name_plural = '注文明細データ'

    def __str__(self):
        return str('%s %s' % (self.order, self.menu))


class OrderDetailStatus(models.Model):

    order_detail = models.ForeignKey(OrderDetail, related_name='order_detail_status', db_constraint=False, on_delete=models.DO_NOTHING)

    # ステータス(現在の処理状況)　作成中に変更したら、取り消し不可にする
    # 食べ放題が終了確認終わったら、Code_999出来上がりに変更する
    status = models.ForeignKey(MasterData, null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.order_detail_status})

    # 現在状況開始時間
    start_time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(SysUser, db_constraint=False, on_delete=models.DO_NOTHING, blank=True, null=True)

    # 可用于排他，在插入新的状态时，确定旧状态是否是当时最新，如果不是，则说明有人改动过状态，处理终止
    current = models.NullBooleanField(default=False)

    class Meta:
        db_table = 'order_detail_status'
        verbose_name = '注文明細'
        verbose_name_plural = '注文明細データ'

# TODO: 注文履歴データ(過去データ、分析用,閉店処理際に、今日の分削除して投入)


class OrderDetailMenuFree(models.Model):
    '''
    OrderDetailの拡張テーブル、放題の注文を管理するため
    放題本体データ登録（明細も同時に登録）
    '''
    # ※为了写SQL方便，同时对order 和 orderdetail都进行关联
    order = models.ForeignKey(Order, related_name='order', db_constraint=False, on_delete=models.DO_NOTHING)

    order_detail = models.ForeignKey(OrderDetail, related_name='order_detail', db_constraint=False, on_delete=models.DO_NOTHING)

    #　食べ放題、関連メニュー設定、データある場合、価格は０円にする
    menu_free = models.ForeignKey(MenuFree, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    # 是否可以开始(注文後＝＞False、確認後＝＞True)
    usable = models.BooleanField(default=False)

    #　利用開始 (TODO 一般で利用開始時間)
    start = models.DateTimeField(null=True, blank=True)

    #　利用終了時間
    # TODO 1，食べ放題の注文可能時間管理用、開始後、終了時間計算し、設定する、設定しない場合、無限時間
    # TODO 2，同样的注文一旦有一个已经确认完了，并且开始之后所有的同桌同种类的注文都按照统一时间设定该项目，
    #         无论开始时间为何时,在计算是否终了的时候，只要同种类随便一个数据的end时间都可以确定
    end = models.DateTimeField(null=True, blank=True)

    #　中途结帐，或者别的原因结束时(该机能暂不实装)
    stop = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'order_detail_menu_free'
        verbose_name = '放題注文明細'
        verbose_name_plural = '放題注文明細データ'


class OrderHistory(models.Model):

    order_no = models.CharField(max_length=20)
    counter_no = models.CharField(max_length=64)
    seat = models.ForeignKey(Seat, null=True, related_name='order_seat_history', db_constraint=False, on_delete=models.DO_NOTHING)
    order_type = models.ForeignKey(MasterData, null=True, blank=True, related_name='order_type_history', db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.order_type})
    order_method = models.ForeignKey(MasterData, null=True, blank=True, related_name='order_method_history', db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.order_method})
    guest = models.ForeignKey(Guest, db_constraint=False, on_delete=models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(SysUser, db_constraint=False, on_delete=models.DO_NOTHING, blank=True, null=True)
    order_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_history'


class OrderDetailHistory(models.Model):

    order = models.ForeignKey(OrderHistory, related_name='order_detail_history', db_constraint=False, on_delete=models.DO_NOTHING)
    menu = models.ForeignKey(Menu, related_name='order_detail_menu_history', db_constraint=False, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    menu_option = JSONField(null=True, blank=True)
    option = JSONField(null=True, blank=True)
    count = models.IntegerField(default=0)
    cancelable = models.NullBooleanField()

    class Meta:
        db_table = 'order_detail_history'


class OrderDetailStatusHistory(models.Model):

    order_detail = models.ForeignKey(OrderDetailHistory, related_name='order_detail_status_history', db_constraint=False, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(MasterData, null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.order_detail_status})
    start_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(SysUser, db_constraint=False, on_delete=models.DO_NOTHING, blank=True, null=True)
    current = models.NullBooleanField(default=False)

    class Meta:
        db_table = 'order_detail_status_history'


class OrderDetailMenuFreeHistory(models.Model):
    order = models.ForeignKey(OrderHistory, related_name='order_history', db_constraint=False, on_delete=models.DO_NOTHING)
    order_detail = models.ForeignKey(OrderDetailHistory, related_name='order_detail_history', db_constraint=False, on_delete=models.DO_NOTHING)
    menu_free = models.ForeignKey(MenuFree, null=True, db_constraint=False, on_delete=models.DO_NOTHING)
    usable = models.BooleanField(default=False)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    stop = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'order_detail_menu_free_history'
