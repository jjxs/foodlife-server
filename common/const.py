
class MasterGroupDomain(object):

    # メニューオプション
    MenuOption = "menu_option"

    # メニューカテゴリー
    MenuCategory = "menu_category"


class MasterGroup(object):

    # 予約種別
    reservation_type = 'reservation_type'

    # 最終学歴
    final_education = 'final_education'

    # 支払方法
    pay_method = 'pay_method'

    # デバイス種別
    device_type = 'device_type'

    # 注文タイプ
    order_type = 'order_type'

    # 顧客レベル
    geust_level = 'geust_level'

    # 注文手段
    order_method = 'order_method'

    # 席タイプ
    seat_type = 'seat_type'

    # 喫煙タイプ
    seat_smoke_type = 'seat_smoke_type'

    # オーダー明細状態
    order_detail_status = 'order_detail_status'

    # メニュー在庫状況
    menu_stock_status = 'menu_stock_status'

    # 食べ飲み放題タイプ
    free_type = 'free_type'

    # 食べ飲み放題タイプ
    system_config = 'system_config'

    # 取消タイプ
    canceled_type = 'canceled_type'

    # 会計削除タイプ（統計用）
    counter_delete_type = "counter_delete_type"


class OrderDetailStatus(object):

    # 確認待ち
    Code_0 = 0

    # 受付
    Code_100 = 100

    # 調理開始
    Code_200 = 200

    # 調理済み
    Code_300 = 300

    # 出来上がり
    Code_999 = 999

    # 取消
    Code_Cancel = -1
