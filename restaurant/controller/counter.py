from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import authentication, permissions, serializers

from master.models.guest import Guest, GuestUser
from master.models.seat import *
from master.models.counter import *
from master.models.order import *
from master.data.system import SystemConfig
from master.models.master import Config, MstReport, MstReportHistory
from master.data.util_tax import UtilTax
import master.data.cache_data as cache_data
from app.db.models.store_table import ShopCost, ShopCostCat
from app.db.models.tbl import TblSupplie

from common.util import Util
from common.log import logger
from common.web.json import JsonResult
from common.views.view import SampleAPIView
from common.permission.controller import UserRoleAuthenticated
import common.sql as Sql

import json
import sys
import channels.layers
from asgiref.sync import async_to_sync
import datetime
import math
from decimal import Decimal
import common.saas as saas
import copy


class CounterParameters:
    '''
        会計用パラーメータ
    '''

    def __init__(self, request):
        self.counter_id = request.data["counter_id"]
        self.is_first = (not (self.counter_id and self.counter_id > 0))
        self.money = request.data["money"]
        self.is_pay = request.data["is_pay"]
        self.is_split = request.data["is_split"]
        self.is_average = request.data["is_average"]
        self.is_input = request.data["is_input"]
        self.is_over = request.data["is_over"]
        self.number = request.data["number"]
        self.user = request.user
        self.takeout = 0
        if 'takeout' in request.data:
            self.takeout = request.data['takeout']

        if "select_ids" in request.data:
            self.select_ids = request.data["select_ids"]

        if "orders_detail" in request.data:
            self.orders_detail = request.data["orders_detail"]

        if "detail" in request.data:
            self.detail = request.data["detail"]

        if "split_detail" in request.data:
            self.split_detail = request.data["split_detail"]

######################### 会計用メソッド  ###################


def check_price(params):

    total = params.money["total"]
    
    eatin = params.money['eatin']
    takeout = params.money['takeout']
    tax_value = UtilTax.tax_value(eatin) + UtilTax.tax_value(takeout, 1)

    if tax_value != params.money["tax_value"]:
        return False

    price = params.money["price"]
    if price != (total + tax_value):
        return False

    price_tax_in = params.money["price_tax_in"]
    amounts_payable = params.money["amounts_payable"]
    if amounts_payable != (price + price_tax_in):
        return False

    cut = params.money["cut"]
    cut_value = params.money["cut_value"]
    if cut > 0:
        if math.floor(amounts_payable * cut / 100) != cut_value:
            return False

    amounts_actually = amounts_payable - cut_value

    reduce_value = params.money["reduce"]
    amounts_actually = amounts_actually - reduce_value
    if amounts_actually != params.money["amounts_actually"]:
        return False

    pay = params.money["pay"]
    change = params.money["change"]
    if change != (pay - amounts_actually):
        return False

    return True


def create_counter(params):

    if params.is_first:
        # 会計作成
        counter = Counter.objects.create(
            is_pay=params.is_pay,
            is_split=params.is_split,
            is_average=params.is_average,
            is_input=params.is_input,
            number=params.number,
            user=params.user
        )
    else:
        # 会計取得(再編集の場合更新する)
        counter = Counter.objects.get(id=params.counter_id)
        counter.is_pay = params.is_pay
        counter.is_split = params.is_split
        counter.is_average = params.is_average
        counter.is_input = params.is_input
        counter.number = params.number
        counter.user = params.user
        counter.save()

    return counter


def reset_counter(is_completed, counter):

    # total_price = Sql.sql_to_one('''
    #     SELECT SUM(history.price * main.pay_count)
    #     FROM counter_detail_order main
    #     LEFT JOIN order_detail_history history ON history.id = main.order_detail_id
    #     WHERE (main.is_delete IS NULL OR (NOT main.is_delete))
    #     AND   history.price > 0
    #     AND   main.is_ready
    #     AND   main.counter_id = %(counter_id)s
    #     ''', {'counter_id': counter.id})

    pay_price = Sql.sql_to_dict('''
        SELECT 
        SUM(amounts_actually) as amounts_actually, 
        SUM(amounts_payable) as amounts_payable, 
        SUM(amounts_actually_tax) as amounts_actually_tax
        FROM counter_detail
        WHERE (canceled is null or (not canceled))
        AND  counter_id = %(counter_id)s
        ''', {'counter_id': counter.id})

    amounts_actually = pay_price[0]['amounts_actually'] if pay_price[0]['amounts_actually'] else 0
    amounts_payable = pay_price[0]['amounts_payable'] if pay_price[0]['amounts_payable'] else 0
    amounts_actually_tax = pay_price[0]['amounts_actually_tax'] if pay_price[0]['amounts_actually_tax'] else 0

    #　実際支払いました金額
    counter.pay_price = amounts_actually
    
    #　支払べき金額(減免前)
    counter.total_price = amounts_payable
    
    #　税金
    counter.tax_price = amounts_actually_tax
    counter.is_completed = is_completed

    counter.save()


def create_counter_detail(params, counter):

    id = params.money["pay_method_id"]
    master = MasterData.objects.get(id=id)

    amounts_actually = params.money["amounts_actually"]

    takeout = params.takeout
    amounts_actually_tax = UtilTax.tax_in(amounts_actually, takeout)
    tax = SystemConfig.fax()
    if takeout:
         tax = SystemConfig.takeout_fax()

    # 会計明細情報作成
    detail = CounterDetail.objects.create(
        no=Util.current_string("%Y%m%d%H%M%S%f"),
        counter=counter,
        pay_method=master,
        tax=tax,
        tax_value=params.money["tax_value"],
        total=params.money["total"],
        price=params.money["price"],
        price_tax_in=params.money["price_tax_in"],
        amounts_payable=params.money["amounts_payable"],
        amounts_actually=params.money["amounts_actually"],
        amounts_actually_tax=amounts_actually_tax,
        pay=params.money["pay"],
        change=params.money["change"],
        cut=params.money["cut"],
        cut_value=params.money["cut_value"],
        reduce=params.money["reduce"],
        user=params.user,
        eatin=params.money["eatin"],
        takeout=params.money["takeout"]
    )

    return detail


def create_counter_detail_order(params, counter, counter_detail):

    # 分割で登録以外のデータをクリアする。
    sql_params = {
        "counter_id": counter.id
    }
    Sql.execute('''
        delete from counter_detail_order 
        where counter_id = %(counter_id)s 
            and counter_detail_id is null
        ''', sql_params)

    # 分割の場合
    if params.is_split:
        for detail in params.split_detail:
            tax = SystemConfig.fax()
            if 'is_takeout' in detail and detail['is_takeout']:
                tax = SystemConfig.takeout_fax()
            # CounterDetailOrder作成
            CounterDetailOrder.objects.create(
                counter=counter,
                counter_detail=counter_detail,  # 分割の場合のみ登録
                order_detail_id=detail["detail_id"],
                pay_count=detail["count"],
                pay_price=detail["price"],
                ori_price=detail['ori_price'],
                tax_in=detail["tax_in"],
                is_delete=detail["is_delete"],
                is_ready=detail["is_ready"],
                tax=tax
            )

    # 分割以外の場合全件新規作成（変更のみの判定いらず、面倒です）
    for detail in params.orders_detail:
        tax = SystemConfig.fax()
        if 'is_takeout' in detail and detail['is_takeout']:
            tax = SystemConfig.takeout_fax()
        # CounterDetailOrder作成, 会計明細（counter_detail）を連携しない
        CounterDetailOrder.objects.create(
            counter=counter,
            order_detail_id=detail["detail_id"],
            pay_count=detail["count"],
            pay_price=detail["price"],
            ori_price=detail['ori_price'],
            tax_in=detail["tax_in"],
            is_delete=detail["is_delete"],
            is_ready=detail["is_ready"],
            tax=tax
        )


def save_order_history(params, counter):

    #　1回目以降の会計は  処理しない
    if not params.is_first:
        return

    # =========================================
    # SQL すべてのorder_detail_idを取得
    sql = '''
    select distinct order_detail.id from "order"
    inner join order_detail on order_detail.order_id = "order".id and "order".seat_id in  %(seat_ids)s
    '''
    detail_ids = Sql.sql_to_list(sql, {"seat_ids": tuple(params.select_ids)})
    sql_params = {"detail_ids": tuple(detail_ids)}

    # OrderDetailStatusHistory
    Sql.execute('''
    insert into order_detail_status_history
    select id, start_time, current, order_detail_id, status_id, user_id
    from order_detail_status where order_detail_id in %(detail_ids)s
    ''', sql_params)

    Sql.execute("delete from order_detail_status where order_detail_id in %(detail_ids)s ", sql_params)

    # =========================================
    # SQL すべてのOrder_idを取得
    sql = '''
    select "order".id from "order" where seat_id in %(seat_ids)s
    '''
    order_ids = Sql.sql_to_list(sql, {"seat_ids": tuple(params.select_ids)})
    sql_params = {"order_ids": tuple(order_ids)}

    # OrderDetailMenuFreeHistory
    Sql.execute('''
    insert into order_detail_menu_free_history
    select id, usable, start, "end", stop, menu_free_id, order_id, order_detail_id
    from order_detail_menu_free where order_id in %(order_ids)s
    ''', sql_params)
    Sql.execute("delete from order_detail_menu_free where order_id in %(order_ids)s ", sql_params)

    # OrderDetailHistory
    Sql.execute('''
    insert into order_detail_history
    select id, price, option, "count", cancelable, menu_id, order_id,ori_price,menu_option
    from order_detail where order_id in %(order_ids)s
    ''', sql_params)
    Sql.execute("delete from order_detail where order_id in %(order_ids)s ", sql_params)

    # OrderHistory
    Sql.execute('''
    insert into order_history
    select id, order_no, counter_no, order_time, guest_id, order_method_id, order_type_id, seat_id, user_id
    from "order" where id in %(order_ids)s
    ''', sql_params)
    Sql.execute('delete from "order" where id in %(order_ids)s ', sql_params)

    return detail_ids


def save_counter_seat(params, counter):

    #　1回目以降の会計は  処理しない
    if not params.is_first:
        return

    # 完了処理の場合のみ、登録処理を行います
    # if not params.is_over:
    #     return False

    # 为了防止在结帐期间 发生再注文，一旦结算处理开始，就将seat_status数据移除，
    # 这样新规的画面就无法找到数据，而既存的画面，发行Websocket通知使用终了

    for id in params.select_ids:
        seat = Seat.objects.get(id=id)
        seat_status = SeatStatus.objects.get(seat=seat)
        CounterSeat.objects.create(
            counter=counter,
            seat_id=seat.id,
            seat_status_id=seat_status.id,
            counter_no=seat_status.counter_no)

    sql_params = {"select_ids": tuple(params.select_ids)}

    # 履歴作成
    Sql.execute('''
    insert into seat_status_history select id, counter_no, start, clock_timestamp(), security_key, seat_id, number, utype
    from seat_status where seat_id in %(select_ids)s
    ''', sql_params)

    # 作成
    Sql.execute("delete from seat_status where seat_id in %(select_ids)s ", sql_params)

    # stop seat free
    sql = "delete from seat_free WHERE seat_id in %(select_ids)s"
    Sql.execute(sql, sql_params )

    return True


class CounterController(SampleAPIView):
    # 認証
    permission_classes = (UserRoleAuthenticated,)

    def sale_count(self, request, *args, **kwargs):
        where_date = '1970-01-01'
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        if 'year' in request.data:
            year = request.data['year']
        if 'month' in request.data:
            month = request.data['month']

        where_start_date = "{0}-{1}-01".format(year, str(month).rjust(2,'0'))

        end_month = 1 if month>11 else month+1
        end_year = year+1 if month>11 else year
        where_end_date = "{0}-{1}-01".format(end_year, str(end_month).rjust(2,'0'))

        details = Sql.sql_to_dict('''
            SELECT DISTINCT counter_detail.id,
                counter_detail.no AS detail_no,
                counter_detail.amounts_payable AS amounts_payable,
                counter_detail.amounts_actually AS amounts_actually,
                counter_detail.pay AS pay,
                counter_detail.change AS change,
                counter_detail.reduce AS reduce,
                counter_detail.cut AS cut,
                counter_detail.cut_value AS cut_value,
                counter_detail.print_count AS print_count,
                master_data.display_name AS pay_name,
                counter.create_time,
                CASE WHEN seat_history.number IS NULL THEN 0 ELSE seat_history.number END as number,
                CAST(counter.create_time AS DATE) AS day
            FROM counter_detail
            LEFT JOIN counter ON counter.id = counter_detail.counter_id
            LEFT JOIN master_data ON counter_detail.pay_method_id = master_data.id
            LEFT JOIN ( SELECT MAX ( number ) AS number, counter_id FROM 
            counter_seat LEFT JOIN seat_status_history ON seat_status_history.counter_no = counter_seat.counter_no GROUP BY counter_id ) AS seat_history ON seat_history.counter_id = counter.id
            
            WHERE (counter."delete" IS NULL OR counter."delete" = FALSE)
            AND   (counter_detail.canceled IS NULL OR counter_detail.canceled = FALSE)
            AND counter.create_time>=%(where_start_date)s AND counter.create_time<%(where_end_date)s
            ORDER BY counter_detail.no ASC 
        ''', {"where_start_date":where_start_date, "where_end_date":where_end_date})

        days = Sql.sql_to_dict('''
            SELECT SUM(amounts_payable) as amounts_payable,
                SUM(amounts_actually) as amounts_actually,
                CAST(counter.create_time AS DATE) AS day,
                SUM(CASE WHEN date_part('hour',counter.create_time)>=8 THEN amounts_actually ELSE 0 END) as dinner,
                SUM(CASE WHEN date_part('hour',counter.create_time)<8 THEN amounts_actually ELSE 0 END) as lunch,
                master_data.display_name,
                SUM(1) as pay_count,
                SUM(counter.number) as number,
                SUM(counter_detail.cut_value) as cut_value,
                SUM(counter_detail.reduce) as reduce,
                counter_detail.pay_method_id
            FROM counter_detail
            LEFT JOIN counter ON counter.id = counter_detail.counter_id
			LEFT JOIN master_data ON counter_detail.pay_method_id=master_data.id
            WHERE (counter."delete" IS NULL OR counter."delete" = FALSE)
            AND   (counter_detail.canceled IS NULL OR counter_detail.canceled = FALSE)
            AND counter.create_time>=%(where_start_date)s AND counter.create_time<%(where_end_date)s
            GROUP BY day, master_data.display_name, counter_detail.pay_method_id 
            ORDER BY day desc, counter_detail.pay_method_id asc 
        ''', {"where_start_date":where_start_date, "where_end_date":where_end_date})
        day_result = {}
        for row in days:
            if row['day'] not in day_result:
                day_result[row['day']] = {
                    'amounts_payable': 0,
                    'amounts_actually': 0,
                    'day' : row['day'],
                    'dinner': 0,
                    'lunch': 0,
                    'pays': [],
                    'number': 0,
                    'cut_value': 0,
                    'reduce': 0,
                }
            day_result[row['day']]['amounts_payable'] += row['amounts_payable'] 
            day_result[row['day']]['amounts_actually'] += row['amounts_actually'] 
            day_result[row['day']]['dinner'] += row['dinner'] 
            day_result[row['day']]['lunch'] += row['lunch']
            day_result[row['day']]['number'] += row['number']
            day_result[row['day']]['cut_value'] += row['cut_value']
            day_result[row['day']]['reduce'] += row['reduce']
            day_result[row['day']]['pays'].append({
                'amounts_actually': row['amounts_actually'],
                'display_name': row['display_name'],
                'count': row['pay_count'],
                'number': row['number']
            })
        
        result = JsonResult(data={
            'days': day_result.values(),
            'details': details
        })

        return Response(result)

    # 回復処理

    def reset(self, request, *args, **kwargs):

        counter_id = request.data["counter_id"]
        counter = Counter.objects.get(id=counter_id)
        counter.delete = None
        counter.user = request.user
        counter.save()

        counters = Sql.sql_to_dict(r'SELECT * FROM counter WHERE id = %(counter_id)s ', {"counter_id": counter_id})

        return Response(counters)

    # 削除処理
    def delete(self, request, *args, **kwargs):

        counter_id = request.data["counter_id"]
        counter = Counter.objects.get(id=counter_id)
        counter.delete = True
        counter.user = request.user
        counter.save()

        counters = Sql.sql_to_dict(r'SELECT * FROM counter WHERE id = %(counter_id)s ', {"counter_id": counter_id})

        return Response(counters)

    # 取消処理
    def cancel(self, request, *args, **kwargs):

        counter_id = request.data["counter_id"]
        sql_params = {
            "counter_id": counter_id
        }
        if "detail_id" in request.data:
            sql_params["counter_detail_id"] = request.data["detail_id"]

        # 事务处理開始
        with transaction.atomic():

            sql_CounterDetail = '''
                UPDATE counter_detail
                SET canceled = TRUE
                WHERE counter_id = %(counter_id)s                 
            '''

            sql_CounterDetailOrder = '''
                UPDATE counter_detail_order 
                SET counter_detail_id = null
                WHERE counter_id =  %(counter_id)s                 
            '''
            if "detail_id" in request.data:
                sql_CounterDetail += "AND   id = %(counter_detail_id)s "
                sql_CounterDetailOrder += " AND counter_detail_id =  %(counter_detail_id)s "

            Sql.execute(sql_CounterDetail, sql_params)
            Sql.execute(sql_CounterDetailOrder, sql_params)

            # 支配金額再計算
            counter = Counter.objects.get(id=counter_id)
            reset_counter(False, counter)

        counters = Sql.sql_to_dict(r'SELECT * FROM counter WHERE id = %(counter_id)s ', sql_params)
        return Response(counters)

    # # 印刷用明細取得
    # def print_details(self, request, *args, **kwargs):

    #     counter_id = request.data["counter_id"]
    #     detail_id = request.data["detail_id"]

    #     params = {
    #         'counter_id': counter_id,
    #         'detail_id': detail_id
    #     }

    #     counter = Counter.objects.get(id=counter_id)
    #     rows = Sql.sql_to_dict('''
    #         SELECT counter_detail.id,
    #             counter_detail.no AS detail_no,
    #             counter_detail.total AS total,
    #             counter_detail.price - counter_detail.total AS tax,
    #             counter_detail.price AS price,
    #             counter_detail.pay AS pay,
    #             counter_detail.change AS change,
    #             counter_detail.reduce AS reduce,
    #             counter_detail.cut AS cut,
    #             master_data.display_name AS pay_name
    #         FROM counter_detail
    #         LEFT JOIN master_data ON counter_detail.pay_method_id = master_data.id
    #         WHERE counter_detail.id = %(detail_id)s
    #     ''', params)

    #     result = rows[0]
    #     result["no_pay"] = False
    #     if counter.is_average or counter.is_input:
    #         # 明細個別印刷できない場合、すべての明細に出力
    #         result['total'] = counter.total_price
    #         result['price'] = counter.pay_price
    #         result['tax'] = counter.tax_price
    #         result['pay'] = 0
    #         result['change'] = 0
    #         result['no_pay'] = True

    #     sql_details = '''
    #         SELECT main.pay_count AS COUNT,
    #             detail.price AS price,
    #             detail.price*main.pay_count AS total,
    #             menu.name AS menu_name,
    #             menu.no AS menu_no
    #         FROM counter_detail_order main
    #         LEFT JOIN order_detail_history detail ON detail.id = main.order_detail_id
    #         LEFT JOIN menu ON menu.id = detail.menu_id
    #         WHERE (main.is_delete IS NULL OR (NOT main.is_delete))
    #         AND   detail.price > 0
    #         AND   main.is_ready
    #         AND   main.counter_id = %(counter_id)s
    #     '''

    #     if counter.is_split:
    #         sql_details += r" AND   main.counter_detail_id = %(detail_id)s "
    #     else:
    #         sql_details += r" AND   main.counter_detail_id IS NULL "

    #     result["details"] = Sql.sql_to_dict(sql_details, params)

    #     return Response(result)

    # 会計画面明細部取得（履歴から取る）

    def edit(self, request, *args, **kwargs):

        sql = Sql.get("get_counter_orders.history")
        params = {
            "counter_id": request.data["counter_id"]
        }
        rows = Sql.sql_to_dict(sql, params)

        return Response(rows)
    
    def get_detail(self, request, *args, **kwargs):

        sql = Sql.get("get_counter_orders.history")
        params = {
            "counter_id": request.data["counter_id"],
        }
        if 'counter_detail_id' in request.data:
            params["counter_detail_id"] = request.data['counter_detail_id']
            sql = Sql.get("get_counter_orders_detail")
        rows = Sql.sql_to_dict(sql, params)

        return Response(rows)

    # 会計画面明細部取得（注文からデータ取る）
    def orders_detail(self, request, *args, **kwargs):
        '''
        会計画面明細取得
        '''
        sql = Sql.get("get_counter_orders")
        params = {
            "seat_ids": tuple(request.data["seat_ids"])
        }
        rows = Sql.sql_to_dict(sql, params)

        return Response(rows)

    # 会計履歴データ取得
    def counter_detail(self, request, *args, **kwargs):

        params = {}

        sql_counters = '''
            SELECT *
            FROM counter
            WHERE 1 = 1     
            {0}
            ORDER BY create_time DESC
        '''

        sql_counter_details = r''' 
            SELECT counter_detail.*,
                (CASE WHEN date_part('hour',counter_detail.create_time)<8 THEN 1 ELSE 0 END) as lunch,
                master_data.code,
                master_data.display_name,
                auth_user.username
            FROM counter_detail
            LEFT JOIN master_data ON counter_detail.pay_method_id = master_data.id
            LEFT JOIN counter ON counter.id = counter_detail.counter_id AND  (counter.delete <> true or delete is null) 
            LEFT JOIN auth_user ON auth_user.id = counter_detail.user_id
            WHERE 1 = 1 
            {0} 
            ORDER BY counter_detail.create_time DESC
            '''

        sql_counter_seat = r'''
            SELECT counter_seat.id,
                counter_seat.counter_id,
                counter_seat.counter_no,
                seat_status_history.start,
                seat_status_history.end,
                seat.id AS seat_id,
                seat.seat_no,
                seat.name seat_name,
                seat_group.id AS group_id,
                seat_group.name AS group_name,
                counter.create_time
            FROM counter_seat
            LEFT JOIN seat_status_history
                    ON seat_status_history.seat_id = counter_seat.seat_id
                    AND seat_status_history.counter_no = counter_seat.counter_no
            LEFT JOIN seat ON seat.id = counter_seat.seat_id
            LEFT JOIN seat_group ON seat.group_id = seat_group.id
            LEFT JOIN counter ON counter.id = counter_seat.counter_id AND ( counter.delete <> true or delete is null )
            WHERE counter_id IS NOT NULL {0} 
            ORDER BY counter.create_time DESC
        '''

        sql_formart_counters = " AND ( counter.delete <> true or delete is null ) "
        sql_formart_counter_details = ""
        sql_formart_counter_seat = ""


        if "year" in request.data:
            start_date = "{0}-{1}-{2} 00:00:00".format(request.data['year'], str(request.data['month']).rjust(2,'0'), str(request.data['day']).rjust(2,'0'))
            end_date   = "{0}-{1}-{2} 23:59:59".format(request.data['year'], str(request.data['month']).rjust(2,'0'), str(request.data['day']).rjust(2,'0'))

            sql_formart_counters += r" AND create_time >= '{0}' AND create_time<= '{1}' ".format(start_date, end_date)
            sql_formart_counter_details += r" AND counter.create_time >= '{0}' AND counter.create_time<= '{1}' ".format(start_date, end_date)
            sql_formart_counter_seat += r" AND counter.create_time >= '{0}' AND counter.create_time<= '{1}' ".format(start_date, end_date)

        # if "today" in request.data and request.data["today"]:
        #     sql_formart_counters += r" AND create_time >= now()::date "
        #     sql_formart_counter_details += r" AND counter.create_time >= now()::date "
        #     sql_formart_counter_seat += r" AND counter.create_time >= now()::date "
        # else:
        #     day30 = (datetime.datetime.now()-datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        #     sql_formart_counters += r" AND create_time >= '" + day30 + "'"
        #     sql_formart_counter_details += r" AND counter.create_time >= '" + day30 + "'"
        #     sql_formart_counter_seat += r" AND counter.create_time >= '" + day30 + "'"

        if "counter_id" in request.data and int(request.data["counter_id"]) > 0:
            counterId = request.data["counter_id"]
            params = {"counter_id": counterId}
            sql_formart_counters += r" AND counter.id = %(counter_id)s "
            sql_formart_counter_details += r" AND counter.id = %(counter_id)s "
            sql_formart_counter_seat += r" and counter_seat.counter_id = %(counter_id)s"

        sql = sql_counters.format(sql_formart_counters)
        counters = Sql.sql_to_dict(sql, params)

        sql = sql_counter_details.format(sql_formart_counter_details)
        counter_details = Sql.sql_to_dict(sql, params)

        sql = sql_counter_seat.format(sql_formart_counter_seat)
        counter_seats = Sql.sql_to_dict(sql, params)

        result = JsonResult(data={
            'counters': counters,
            'counter_details': counter_details,
            'counter_seats': counter_seats,

        })

        return Response(result)

    # モニター通知
    def notice_monitor(self, request, *args, **kwargs):

        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            saas.group_name(saas.id(request), '__CounterConsumer__'),
            {
                'type': 'sendPrice',
                'data': {
                    'type': request.data["type"],
                    'faxprice': request.data["faxprice"],
                    'price': request.data["price"],
                    'pay': request.data["pay"],
                    'change': request.data["change"],
                }
            })
        return Response()

    def counter(self, request, *args, **kwargs):
        '''
            会計処理
        '''

        params = CounterParameters(request)

        if not check_price(params):
            return Response(JsonResult(result=False, message="金額計算不正、ご確認してください。"))


        # 事务处理開始
        with transaction.atomic():
            # 会計 テーブル取得または登録　
            counter = create_counter(params)

            # 席情報履歴作成登録する
            save_counter_seat(params, counter)

            # 会計明細情報作成
            counter_detail = create_counter_detail(params, counter)

            # 会計関連注文情報登録する
            create_counter_detail_order(params, counter, counter_detail)

            # TODO:
            # 终了结算的时候，應該检查结帐桌号里面，是否还有create_counter_detail_order中不存在的注文明細數據
            # 該數據有可能是在結算開始到第一次結算發生前，客戶誤操作所產生的
            # 但考慮到該情況發生可能性較小，暫不對應以後版本追加功能

            # 注文情報履歴登録
            detail_ids = save_order_history(params, counter)

            # 会計合計情報統計
            reset_counter(params.is_over, counter)

        # モニターに通知
        try:
            channel_layer = channels.layers.get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                saas.group_name(saas.id(request), '__CounterConsumer__'),
                {
                    'type': 'sendPrice',
                    'data': {
                        "type": "over"
                    }
                })

            # 席の利用を中止
            for seat_id in params.select_ids:
                group_name = saas.group_name(saas.id(request), "__SeatConsumer__{0}".format(seat_id))
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        'type': 'seat_using_stop'
                    })

            #　キチン監視画面同期
            async_to_sync(channel_layer.group_send)(
                saas.group_name(saas.id(request), '__KitchenConsumer__'),
                {
                    'type': 'order_delete',
                    'detail_id': Util.encode(detail_ids)
                })
        except:
            print(sys.exc_info()[0])

        result = JsonResult(result=True, message="会計が完了しました。", data=Util.model_to_dict(counter_detail))
        return Response(result)


    def print_count(self, request, *args, **kwargs):
        if 'id' in request.data:
            id = request.data['id']
            obj = CounterDetail.objects.get(id=id)
            obj.print_count = int(obj.print_count or 0) + 1
            obj.save()
        result = JsonResult(result=True, message="処理しました")
        return Response(result)

    def get_supplie(self):
        sql = "SELECT sup_name, sup_tel, sup_addr FROM tbl_supplie"
        result = Sql.sql_to_dict(sql=sql)
        return result

    def get_cash_record(self, request, *args, **kwargs):

        search_key = 'cash_record'
        data = {}
        if 'date' in request.data:
            reports = MstReport.objects.filter(report_type='counter_daily', report_date=request.data['date']).order_by("-id")
            if reports.count()>0:
                data = reports[0].report
        data['supplie'] = self.get_supplie()
        result = JsonResult(result=True, message="処理しました", data=data)
        return Response(result)


    def cash_record(self, request, *args, **kwargs):
        # 事务处理開始
        with transaction.atomic():
            report_date = request.data['date'][0:10]
            # save report
            counterDailys = MstReport.objects.filter(report_type='counter_daily', report_date=report_date)
            counterDaily = MstReport()
            if counterDailys.count()>0:
                counterDaily = counterDailys[0]
            counterDaily.report_type = 'counter_daily'
            counterDaily.report_date = report_date
            counterDaily.report = request.data
            counterDaily.save()
            
            counterDailyHistory = MstReportHistory()
            counterDailyHistory.report_type = 'counter_daily'
            counterDailyHistory.report_date = report_date
            counterDailyHistory.report = request.data
            counterDailyHistory.save()

            # save ある時,保存
            if 'save' in request.data and request.data['save']==1:
                # 費用データ保存
                shop_cost_catid = 0
                arr = ShopCostCat.objects.filter(category_name='日常')
                if arr.count()==0:
                    shopCostCat = ShopCostCat()
                    shopCostCat.category_name = '日常'
                    shopCostCat.save()
                else:
                    shopCostCat = arr[0]

                if 'orders' in request.data:
                    for item in request.data['orders']:
                        shopCost = ShopCost()
                        shopCost.cost_category_id = shopCostCat.id
                        shopCost.cost_name = item['name']
                        shopCost.cost = item['amount']
                        shopCost.pay_time = report_date
                        shopCost.save()

        result = JsonResult(result=True, message="処理しました")
        return Response(result)
