from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import authentication, permissions, serializers

from master.models.guest import Guest, GuestUser
from master.models.seat import Seat, SeatStatus
from master.serializer.seat import SeatSerializer, SeatStatusSerializer

from common.util import Util
from common.log import logger
from common.web.json import JsonResult
from common.views.view import SampleAPIView
from common.permission.controller import UserRoleAuthenticated
import common.sql as Sql

import master.data.cache_data as cache_data
import datetime


class ChartsController(SampleAPIView):
    # 認証
    permission_classes = (UserRoleAuthenticated,)

    # 遅い処理をSQL＋キャッシュ化する
    def total(self, request, *args, **kwargs):
        # menulist = cache_data.get_menu_list()
        # if menulist:
        #     return Response(menulist)

        sql = '''
            SELECT CAST(counter.create_time AS DATE) AS date,
            SUM(pay_price) as total_pay_price,
            count( distinct(counter.id)) as total_counter,
            SUM(p.person) as total_person
            FROM counter
            left JOIN (
                select SUM(CASE WHEN seat_status_history.number IS NULL THEN 0 ELSE seat_status_history.number END) as person ,counter_seat.counter_id 
                from counter_seat 
                left JOIN seat_status_history ON seat_status_history.counter_no = counter_seat.counter_no
                group by counter_seat.counter_id 
            ) p on counter.id = p.counter_id
            WHERE create_time >  current_date - interval '30' day
            GROUP BY date 
            ORDER BY date ASC
        '''
        menulist = Sql.sql_to_dict(sql)
        # cache_data.set_menu_list(menulist)
        # print(menulist)
        return Response(menulist)

    # 曜日別売上統計表
    def week(self, request, *args, **kwargs):
        params = {
            'start_date': request.GET['start_date'],
            'end_date': request.GET['end_date'] + ' 23:59:59'
        }
        sql = '''
            SELECT CAST(counter.create_time AS DATE) AS date,
            SUM(pay_price) as pay_price,
            count(1) as counter,
            SUM(CASE WHEN seat_status_history.number IS NULL THEN 0 ELSE seat_status_history.number END) as person,
            SUM(CASE WHEN date_part('hour',counter.create_time)>=8 THEN 1 ELSE 0 END) as counter_dinner,
            SUM(CASE WHEN date_part('hour',counter.create_time)<8 THEN 1 ELSE 0 END) as counter_lunch,
            SUM(CASE WHEN date_part('hour',counter.create_time)>=8 THEN pay_price ELSE 0 END) as pay_price_dinner,
            SUM(CASE WHEN date_part('hour',counter.create_time)<8 THEN pay_price ELSE 0 END) as pay_price_lunch,
            SUM(CASE WHEN date_part('hour',counter.create_time)>=8 THEN seat_status_history.number ELSE 0 END) as person_dinner,
            SUM(CASE WHEN date_part('hour',counter.create_time)<8 THEN seat_status_history.number ELSE 0 END) as person_lunch
            FROM counter
            LEFT JOIN counter_seat ON counter.id = counter_seat.counter_id
            LEFT JOIN seat_status_history ON seat_status_history.counter_no = counter_seat.counter_no
            WHERE create_time >=  %(start_date)s AND create_time <= %(end_date)s
            GROUP BY date 
            ORDER BY date ASC
        '''
        menulist = Sql.sql_to_dict(sql, params)
        # cache_data.set_menu_list(menulist)
        # print(menulist)
        return Response(menulist)

    # 日別売上統計表
    def day(self, request, *args, **kwargs):
        sql_condition = []
        if 'light' in request.GET:
            light = request.GET['light']
            night = request.GET['night']

            if light == '1' and night == '1':
                pass
            elif light == '1':
                sql_condition.append(
                    " AND date_part('hour', counter.create_time) < 8 ")
            elif night == '1':
                sql_condition.append(
                    " AND date_part('hour', counter.create_time) >= 8 ")

        params = {
            'start_date': request.GET['start_date'],
            'end_date': request.GET['end_date'] + ' 23:59:59'
        }
        sql = '''
            SELECT CAST(counter.create_time AS DATE) AS date,
                SUM(counter_detail.amounts_actually) as pay_price,
                count( distinct(counter.id)) as counter,
                SUM(p.person) as person,
                SUM(CASE WHEN counter_detail.pay_method_id = 127 THEN counter_detail.amounts_actually ELSE 0 END) AS paypay_price,
	            SUM(CASE WHEN counter_detail.pay_method_id = 51 THEN counter_detail.amounts_actually ELSE 0 END) AS money_price,
	            SUM(CASE WHEN counter_detail.pay_method_id <> 127 and counter_detail.pay_method_id <> 51 THEN counter_detail.amounts_actually ELSE 0 END) AS other_price
            FROM counter
            left JOIN (
                select SUM(CASE WHEN seat_status_history.number IS NULL THEN 0 ELSE seat_status_history.number END) as person ,counter_seat.counter_id 
                from counter_seat 
                left JOIN seat_status_history ON seat_status_history.counter_no = counter_seat.counter_no
                group by counter_seat.counter_id 
            ) p on counter.id = p.counter_id
            LEFT JOIN counter_detail ON counter.id = counter_detail.counter_id
            LEFT JOIN master_data ON counter_detail.pay_method_id = master_data.id
            WHERE counter.create_time >=  %(start_date)s AND counter.create_time <= %(end_date)s
            AND (counter."delete" IS NULL OR counter."delete" = FALSE)
            AND counter_detail.canceled IS NOT TRUE
            {0}
            GROUP BY date 
            ORDER BY date ASC
        '''

        menulist = Sql.sql_to_dict(sql.format('\n'.join(sql_condition)), params)
        # cache_data.set_menu_list(menulist)
        # print(menulist)
        return Response(menulist)

    # 月別売上統計表
    def month(self, request, *args, **kwargs):
        return self.day(request, args, kwargs)

        # 料理売上統計表
    def cat(self, request, *args, **kwargs):
        sql = '''
            SELECT 
                menu_category.category_id AS cat_id,
                master_data.display_name AS cat_name,
                SUM(1) as total, 
                SUM(ranking.total_price) as total_price, 
                SUM(ranking.dinner) as dinner, 
                SUM(ranking.lunch) as lunch
            FROM (
                select 1, odh.menu_id , (odh.price * count) total_price,
                    (CASE WHEN date_part('hour',counter.create_time)>=8 THEN (odh.price * count) ELSE 0 END) as dinner,
                    (CASE WHEN date_part('hour',counter.create_time)<8 THEN (odh.price * count) ELSE 0 END) as lunch
                    FROM order_detail_history  odh
                    INNER JOIN order_history oh ON oh.id = odh.order_id
                    INNER JOIN counter_detail_order cdo ON cdo.order_detail_id = odh.id
                    INNER JOIN counter_detail ON counter_detail.counter_id = cdo.counter_id
                    INNER JOIN counter ON counter.id = counter_detail.counter_id AND counter.create_time >=  %(start_date)s AND counter.create_time <= %(end_date)s
                    LEFT JOIN counter_seat ON counter.id = counter_seat.counter_id
                    LEFT JOIN seat_status_history ON seat_status_history.counter_no = counter_seat.counter_no
                    WHERE (counter."delete" IS NULL OR counter."delete" = FALSE)
                    AND   (counter_detail.canceled IS NULL OR counter_detail.canceled = FALSE)
            ) as ranking
            LEFT JOIN menu ON menu.id = ranking.menu_id
            LEFT JOIN menu_category ON menu.id = menu_category.menu_id
            LEFT JOIN master_data ON master_data.id = menu_category.category_id
            INNER JOIN master_data_group mdg ON mdg.id = master_data.group_id AND mdg.domain = 'menu_category' AND mdg.id IN %(group_ids)s
            GROUP BY cat_id, master_data.display_name
        '''

        params = {
            'start_date': request.GET['start_date'],
            'end_date': request.GET['end_date'] + ' 23:59:59'
        }
        if 'group' not in request.GET or not request.GET['group']:
            return Response([])
        else:
            params['group_ids'] = tuple(request.GET['group'].split(','))
        menulist = Sql.sql_to_dict(sql, params)
        return Response(menulist)

    # 料理売上統計表
    def menu(self, request, *args, **kwargs):
        sql = '''
            SELECT 
                menu.id AS menu_id,
                menu.name AS menu_name,
                menu.price AS menu_price,
                ranking.total, ranking.total_price, ranking.dinner, ranking.lunch
            FROM (
                select sum(count) total, odh.menu_id , sum(odh.price * count) total_price,
                    SUM(CASE WHEN date_part('hour',counter.create_time)>=8 THEN (odh.price * count) ELSE 0 END) as dinner,
                    SUM(CASE WHEN date_part('hour',counter.create_time)<8 THEN (odh.price * count) ELSE 0 END) as lunch
                    FROM order_detail_history  odh
                    INNER JOIN order_history oh ON oh.id = odh.order_id
                    INNER JOIN counter_detail_order cdo ON cdo.order_detail_id = odh.id
                    INNER JOIN counter_detail ON counter_detail.counter_id = cdo.counter_id
                    INNER JOIN counter ON counter.id = counter_detail.counter_id AND counter.create_time >=  %(start_date)s AND counter.create_time <= %(end_date)s
                    LEFT JOIN counter_seat ON counter.id = counter_seat.counter_id
                    LEFT JOIN seat_status_history ON seat_status_history.counter_no = counter_seat.counter_no
                    WHERE (counter."delete" IS NULL OR counter."delete" = FALSE)
                    AND   (counter_detail.canceled IS NULL OR counter_detail.canceled = FALSE)
                    group by odh.menu_id order by sum(count) desc
            ) as ranking
            LEFT JOIN menu ON menu.id = ranking.menu_id
        '''
        params = {
            'start_date': request.GET['start_date'],
            'end_date': request.GET['end_date'] + ' 23:59:59'
        }

        if request.GET['menu_categorys']:
            sql = sql + ''' LEFT JOIN menu_category cat ON cat.menu_id = menu.id
                            WHERE cat.category_id IN %(menu_categorys)s
                            GROUP BY menu.id,ranking.total, ranking.total_price, ranking.dinner, ranking.lunch
            '''

            params['menu_categorys'] = tuple(
                request.GET['menu_categorys'].split(","))

        menulist = Sql.sql_to_dict(sql, params)
        return Response(menulist)

    def cost(self, request, *args, **kwargs):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        if 'year' in request.data:
            year = request.data['year']
        if 'month' in request.data:
            month = request.data['month']

        where_start_date = "{0}-{1}-01".format(year, str(month).rjust(2, '0'))

        end_month = 1 if month > 11 else month+1
        end_year = year+1 if month > 11 else year
        where_end_date = "{0}-{1}-01".format(end_year,
                                             str(end_month).rjust(2, '0'))

        sql = '''
            SELECT 
                cost.id,
                cost.cost_name,
                cost.cost_category_id,
                cat.category_name,
                cost.pay_time,
                cost.cost
            FROM shop_cost cost
            LEFT JOIN shop_cost_category cat ON cost.cost_category_id = cat.id
            WHERE cost.pay_time >= TIMESTAMP WITH TIME ZONE %(start_date)s AT TIME ZONE 'UTC+9' AND cost.pay_time <= TIMESTAMP WITH TIME ZONE %(end_date)s AT TIME ZONE 'UTC+9'
        '''
        params = {
            'start_date': where_start_date,
            'end_date': where_end_date
        }
        menulist = Sql.sql_to_dict(sql, params)
        return Response(menulist)

    # 料理売上利益統計表
    def profit(self, request, *args, **kwargs):
        sql = '''
            SELECT 
                menu.id AS menu_id,
                menu.name AS menu_name,
                menu.price AS menu_price,
                ranking.total,
                ranking.total_price,
                ranking.dinner,
                ranking.lunch,
                ranking.total_cost
            FROM (
                select 
                    sum(count) total,
                    odh.menu_id,
                    sum(odh.price * count) total_price,
                    SUM(CASE WHEN date_part('hour',counter.create_time)>=8 THEN (odh.price * count) ELSE 0 END) as dinner,
                    SUM(CASE WHEN date_part('hour',counter.create_time)<8 THEN (odh.price * count) ELSE 0 END) as lunch,
                    SUM(costs.cost * count) as total_cost
                FROM
                    order_detail_history  odh
                INNER JOIN
                    order_history oh
                ON
                    oh.id = odh.order_id
                INNER JOIN
                    counter_detail_order cdo
                ON
                    cdo.order_detail_id = odh.id
                INNER JOIN
                    counter_detail
                ON
                    counter_detail.counter_id = cdo.counter_id
                INNER JOIN
                    counter
                ON
                    counter.id = counter_detail.counter_id
                AND
                    counter.create_time >=  %(start_date)s
                AND
                    counter.create_time <= %(end_date)s
                LEFT JOIN
                    counter_seat
                ON
                    counter.id = counter_seat.counter_id
                LEFT JOIN
                    seat_status_history
                ON
                    seat_status_history.counter_no = counter_seat.counter_no
                LEFT JOIN (
                    SELECT 
                        tbr.menu_id as menu_id,
                        sum(ing.ave_price * tbr.amount_to_use) as cost
                    FROM
                        tbl_recipe tbr
                    LEFT JOIN
                        mst_ingredients ing
                    ON
                        tbr.ing_id = ing.id
                    GROUP BY
                        tbr.menu_id
                ) as costs
                ON
                    odh.menu_id = costs.menu_id
                WHERE
                    (counter."delete" IS NULL OR counter."delete" = FALSE)
                AND
                    (counter_detail.canceled IS NULL OR counter_detail.canceled = FALSE)
                group by
                    odh.menu_id
                order by
                    sum(count) desc
            ) as ranking
            LEFT JOIN
                menu
            ON
                menu.id = ranking.menu_id
        '''
        params = {
            'start_date': request.GET['start_date'],
            'end_date': request.GET['end_date'] + ' 23:59:59'
        }
        menulist = Sql.sql_to_dict(sql, params)

        sql = '''
            SELECT 
                menu.id AS menu_id,
                menu.name AS menu_name,
                sum(ing.ave_price * tbr.amount_to_use) as cost
            FROM
                menu
            LEFT JOIN
                tbl_recipe tbr
            ON
                menu.id = tbr.menu_id
            LEFT JOIN
                mst_ingredients ing
            ON
                tbr.ing_id = ing.id
            GROUP BY
                menu.id
        '''
        costs = Sql.sql_to_dict(sql)

        result = {
            'menulist': menulist,
            'costs': costs
        }

        return Response(result)

    # 料理売上統計表
    def table(self, request, *args, **kwargs):
        sql = '''
            SELECT 
                seat.id AS table,
                seat.name AS seat_name,
                seat.seat_no AS seat_no,
                ranking.total, ranking.total_price, ranking.dinner, ranking.lunch
            FROM (
                select sum(count) total, oh.seat_id, sum(odh.price * count) total_price,
                    SUM(CASE WHEN date_part('hour',counter.create_time)>=8 THEN (odh.price * count) ELSE 0 END) as dinner,
                    SUM(CASE WHEN date_part('hour',counter.create_time)<8 THEN (odh.price * count) ELSE 0 END) as lunch
                    FROM order_detail_history  odh
                    INNER JOIN order_history oh ON oh.id = odh.order_id
                    INNER JOIN counter_detail_order cdo ON cdo.order_detail_id = odh.id
                    INNER JOIN counter_detail ON counter_detail.counter_id = cdo.counter_id
                    INNER JOIN counter ON counter.id = counter_detail.counter_id AND counter.create_time >=  %(start_date)s AND counter.create_time <= %(end_date)s
                    LEFT JOIN counter_seat ON counter.id = counter_seat.counter_id
                    LEFT JOIN seat_status_history ON seat_status_history.counter_no = counter_seat.counter_no
                    WHERE (counter."delete" IS NULL OR counter."delete" = FALSE)
                    AND   (counter_detail.canceled IS NULL OR counter_detail.canceled = FALSE)
                    group by oh.seat_id order by sum(count) desc
            ) as ranking
            LEFT JOIN seat ON seat.id = ranking.seat_id
            ORDER BY seat_no
        '''
        params = {
            'start_date': request.GET['start_date'],
            'end_date': request.GET['end_date'] + ' 23:59:59'
        }
        menulist = Sql.sql_to_dict(sql, params)
        return Response(menulist)

    # 棚卸統計表
    def inventory_profit(self, request, *args, **kwargs):
        sql = '''
            select 
                to_char(inventory_date,'YYYY/MM') idate,
                parts_inventory_actual*ave_price as price,
                part_id 
            from public.profit_inventory_detail 
            where to_date(to_char(inventory_date,'YYYY/MM'),'YYYY/MM') <= to_date(%(end_date)s,'YYYY/MM')
            and to_date(to_char(inventory_date,'YYYY/MM'),'YYYY/MM') >= to_date(%(start_date)s,'YYYY/MM')
            order by inventory_date desc,part_id desc
        '''
        params = {
            'start_date': request.GET['start_date'],
            'end_date': request.GET['end_date']
        }
        dataList = Sql.sql_to_dict(sql, params)
        return Response(dataList)