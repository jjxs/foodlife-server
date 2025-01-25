from django.db import models
from django.contrib.auth.models import User as SysUser
from django.contrib.postgres.fields import JSONField
from master.models.menu import Menu
from master.models.guest import Guest
from master.models.seat import Seat, SeatStatusHistory
from master.models.master import MasterData,  MasterDataGroup
from master.models.order import Order, OrderDetail, OrderDetailHistory
import common.const as Const
# 会計関連テーブル


class Counter(models.Model):
    '''
        会計
    '''
    # 一括払い
    is_pay = models.NullBooleanField()

    # 分割 => TODO 新しいデータを作成（from_counter_noに親登録）、明細も分割内容により新しいく作成
    is_split = models.NullBooleanField()

    # 平均割勘 => TODO 平均金額で、新しいデータを作成（from_counter_noに親登録）
    is_average = models.NullBooleanField()

    # 手動設定
    is_input = models.NullBooleanField()

    # 人数（平均割勘、手動用）
    number = models.IntegerField(default=0)

    create_time = models.DateTimeField(auto_now_add=True)

    # 实付金额合计
    pay_price = models.IntegerField(default=0)

    # 应付金额合计
    total_price = models.IntegerField(default=0)

    # 合計税金計算値
    tax_price = models.IntegerField(default=0)

    # 支払完了であるかどうか判定
    is_completed = models.NullBooleanField()

    # 統計用
    delete = models.NullBooleanField()

    # 統計用
    delete_type = models.ForeignKey(MasterData, related_name="delete_type", null=True, db_constraint=False,
                                    on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.counter_delete_type})

    # 管理担当
    user = models.ForeignKey(SysUser, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'counter'


class CounterSeat(models.Model):
    '''
        会計テーブル情報
        支払い完了後、該当テーブルを登録する
    '''
    counter = models.ForeignKey(Counter, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    seat_id = models.IntegerField(default=0)

    # 履歴検索用
    seat_status_id = models.IntegerField(default=0)

    counter_no = models.CharField(max_length=64)

    # 会計テーブル状況
    class Meta:
        db_table = 'counter_seat'


class CounterDetail(models.Model):
    '''
        会計明細情報
        支払 ＝＞　1:1
        分割 ＝＞　1:N
        平均 ＝＞　1:N
        分割 ＝＞　1:N 
    '''
    counter = models.ForeignKey(Counter, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    # 管理、印刷用No
    no = models.CharField(max_length=64, null=True)

    # 支払方法（カード、現金など）
    pay_method = models.ForeignKey(MasterData, related_name="pay_method", null=True, db_constraint=False, on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.pay_method})

    # 税率
    tax = models.DecimalField(max_digits=3, null=True, decimal_places=0)

    # 税額 total * tax
    tax_value = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 支払価格(税抜)　計算した価格（税込メニュー除く
    total = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 支払金額（税込み total + tax_value　（税込メニュー除く
    price = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 税込み金額（税込メニュー金額
    price_tax_in = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 应付金额（price + price_tax_in - cut_value - reduce
    amounts_payable = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 实付金额（price + price_tax_in - cut_value - reduce
    amounts_actually = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 实付金额(税金)
    amounts_actually_tax = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 預り(入金
    pay = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # お釣り
    change = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 割引額(割引値、例：10%)
    cut = models.DecimalField(max_digits=3, null=True, decimal_places=0)

    # 割引額(金額、例：500円) => 明細用
    cut_value = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 減額
    reduce = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 管理担当
    user = models.ForeignKey(SysUser, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    # 取消しました
    canceled = models.NullBooleanField()

    # 取消タイプ
    canceled_type = models.ForeignKey(MasterData, related_name="canceled_type", null=True, db_constraint=False,
                                      on_delete=models.DO_NOTHING, limit_choices_to={'group__name': Const.MasterGroup.canceled_type})
    
    
    # Print Count
    print_count = models.IntegerField(default=0)

    # 支払時間
    create_time = models.DateTimeField(auto_now_add=True)

    # 店内
    eatin = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 持ち帰り
    takeout = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 会計明細
    class Meta:
        db_table = 'counter_detail'


class CounterDetailOrder(models.Model):
    '''    
        会計関連注文情報



        ■ 支払 
        ＝＞　counter　連携　
        ＝＞　counter_detail　設定なし (CounterDetailと関連せず、一回目全件登録する、登録後、画面修正不可になる「編集」利用できない)　   

        ■ 分割 
        ＝＞　counter　連携　
        ＝＞　counter_detail　設定する (CounterDetailと関連する)
        ＝＞  取消する場合　設定を外す

        ■ 平均 
        ＝＞　counter　連携　
        ＝＞　counter_detail　設定なし (CounterDetailと関連せず、一回目全件登録する、登録後、画面修正不可になる「編集」利用できない)　


        ■ 分割 
        ＝＞　counter　連携　
        ＝＞　counter_detail　設定なし (CounterDetailと関連せず、一回目全件登録する、登録後、画面修正不可になる「編集」利用できない)　

    '''

    counter = models.ForeignKey(Counter, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    # 分割会計する場合設定する
    counter_detail = models.ForeignKey(CounterDetail, null=True, db_constraint=False, on_delete=models.DO_NOTHING)

    order_detail_id = models.IntegerField(default=0)

    # 数量(支払数量) =>間違い注文、サービスなどにより、編集
    pay_count = models.IntegerField(default=0)

    # 数量(支払数量) =>間違い注文、サービスなどにより、編集(その他注文編集)
    pay_price = models.DecimalField(max_digits=8, null=True, decimal_places=0)

    # 原始金額（主な利用通貨で、他国通貨への為替はConfifで定義した為替で決まる）
    ori_price = models.DecimalField(max_digits=8, decimal_places=0)
    
    # 注文際に、税金含まれているかどうか（あとから修正可能性あるため、会計時点で記録する）
    tax_in = models.BooleanField(default=False)

    # 手動編集で消す注文、
    is_delete = models.NullBooleanField()

    # 間違い注文(注文したけど、未調理の注文、未完成の注文など)で消す
    is_ready = models.NullBooleanField()

    # 個数分けて登録されている場合
    is_split = models.NullBooleanField()

    # 税率
    tax = models.DecimalField(max_digits=3, null=True, decimal_places=0)

    class Meta:
        db_table = 'counter_detail_order'

