
import datetime
from zipfile import is_zipfile

from botocore import model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
import app.util as Util
from app.db.models.store_table import (
    Takeout, TakeoutOrder, TakeoutOrderDetail, TakeoutUser, Seat)
from app.exception.web import WebException
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, serializers
import hashlib
import json
import base64
from django.contrib.auth import hashers
import googlemaps


from rest_framework_jwt.settings import api_settings
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


UserModel = get_user_model()


class TakeoutApi(BaseAPI):
    permission_classes = (permissions.AllowAny,)

    def login(self, request, params):
        return self.do_login(params, params['username'], params['password'])

    def get_user_info(self, request, params):
        r = jwt_decode_handler(params['token'])
        result = {}
        sql_user = '''
        SELECT
            id,
            seat_no,
            user_address,
            user_email,
            user_id,
            user_name,
            user_tel,
            create_time
        FROM takeout_user
        WHERE
            id = %(id)s
            '''

        result_user = SQL.sql_to_list(sql=sql_user, params={'id': r['id']})
        status = False
        if len(result_user):
            user = result_user[0]
            if user['user_name'] == r['user_name'] and user['seat_no'] == r['seat_no'] and user['user_id'] == r['user_id']:
                result = user
                status = True
        return JsonResponse(result=status, data=result)

    def register(self, request, params):
        username = params["user_id"]
        # 登录名称重複チェック
        exist = self.check_exist_userid(username)
        if exist:
            return JsonResponse(result=False, message='入力された名前がすでに存在します')
        else:
            self.set_takeout_user(params)
            return self.do_login(params, username, params["password"])

    def check_exist_userid(self, params):
        '''重複チェック'''

        DATA_BASE = 'ami'
        sql_param = {}
        sql_condition = []

        sql = '''
        SELECT
            COUNT(0)
        FROM
            takeout_user
        WHERE
            user_id = %(user_id)s
        '''

        sql_param['user_id'] = params
        result = SQL.sql_to_one(sql=sql, params=sql_param, DB_name=DATA_BASE)

        if result > 0:
            return True
        else:
            return False

    def do_login(self, params, username, pwd):
        # login in by takeout user
        # select userid from database, and check password
        # first = base64.b64encode('{"typ":"JWT","alg":"HS256"}')
        # second = base64.b64encode(
        #     '{"user_id":'+username+',"username":"'+pwd+'"}')
        # third = hashlib.sha256
        # result = {token: first+'.' + second+'.'+third}
        result_user = []
        DATA_BASE = 'ami'

        sql_user = '''
        SELECT
            *
        FROM takeout_user
        WHERE
            user_id = %(user_id)s
            '''

        result_user = SQL.sql_to_list(
            sql=sql_user, params={'user_id': username}, DB_name=DATA_BASE)

        result = {}
        status = False
        if len(result_user):
            password = result_user[0].pop('user_pass')
            create_time = result_user[0].pop("create_time")
            data = result_user[0]
            jwt = jwt_encode_handler(data)
            if hashers.check_password(params['password'], password):
                result = {'token': jwt, 'userinfo': data}
                status = True
        return JsonResponse(result=status, data=result)

    def set_takeout_user(self, params):
        '''ユーザーデータ保存'''

        DATA_BASE = 'ami'

        user = UserModel()
        takeout_user = TakeoutUser()
        seat = Seat()

        if'password' in params and params['password']:
            user.set_password(params['password'])
            takeout_user.user_pass = user.password

        # 添加默认坐席
        seat.id = seat.next_value()
        seat.seat_no = self.get_max_company()
        seat.name = params['user_name']
        seat.start = datetime.datetime.now()
        seat.usable = True
        seat.takeout_type = 1
        seat.save()

        # 添加用户
        takeout_user.user_id = params['user_id']
        takeout_user.user_name = params['user_name']
        takeout_user.user_tel = params['user_tel']
        takeout_user.user_address = params['user_address']
        takeout_user.user_email = params['user_email']
        takeout_user.create_time = datetime.datetime.now()
        takeout_user.seat_no = seat.id
        takeout_user.save()

        return user.password

    def get_max_company(self):
        DATA_BASE = 'ami'
        number = 0
        sql = '''
          SELECT
            COALESCE (max(seat_no),'0') AS max
        FROM
            seat
        WHERE 
             takeout_type= 1
        '''
        seatgroup_list = SQL.sql_to_list(sql=sql, params={}, DB_name=DATA_BASE)
        if(len(seatgroup_list) > 0):

            number = int(seatgroup_list[0]['max'])+1
        if(number > 100001):
            return number
        else:
            return 100001

    def get_takeout_data(self, request, params):
        '''takeoutデータ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
           *
        FROM menu
        WHERE takeout=1
        ORDER BY id
        '''
        # sql = sql.format('\n'.join(sql_condition))

        result = SQL.sql_to_list(
            sql=sql, params=sql_param, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def get_confirm_user_data(self, request, params):
        '''获取确认订单页面用户数据'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
           *
        FROM takeout_user
        where user_id = %(user_id)s
        '''
        sql_param['user_id'] = params['userid']

        result = SQL.sql_to_list(
            sql=sql, params=sql_param, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)

    def set_confirm_data(self, request, params):
        '''确认订单后保存数据'''

        DATA_BASE = 'ami'

        takeout_order = TakeoutOrder()

        # 订单表
        takeout_order.id = takeout_order.next_value()
        takeout_order.ship_name = params['user_name']
        taketime = datetime.datetime.now()
        takeout_order.ship_time = str(
            taketime.year) + '-' + str(taketime.month)+'-' + str(taketime.day)+' '+params['user_time']
        takeout_order.ship_tel = params['user_tel']
        takeout_order.user_id = self.get_user_id(params)
        takeout_order.create_time = taketime
        takeout_order.pay_status = '0'
        takeout_order.order_status = '0'
        takeout_order.delivery_type = int(params['delivery_type'])
        if int(params['delivery_type']) == 1:
            takeout_order.ship_addr = params['user_address']
            
            can_ship = self.check_ship_addr(takeout_order.ship_addr)
            if not can_ship:
                return JsonResponse(result=False, message='距離が遠いから、発送できませんでした。')

        takeout_order.save()
        # 订单菜品表
        for neworderlist in params['orderlist']:
            takeout_order_detail = TakeoutOrderDetail()
            takeout_order_detail.order_id = takeout_order.id
            takeout_order_detail.menu_id = neworderlist['id']
            takeout_order_detail.menu_name = neworderlist['name']
            takeout_order_detail.price = neworderlist['price']
            takeout_order_detail.count = neworderlist['newcount']
            takeout_order_detail.create_time = taketime
            takeout_order_detail.save()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def check_ship_addr(self, addr):
        gmaps = googlemaps.Client(key='AIzaSyBmXEEWM1Be4japAKwhd23piFRukY-irpM')

        # Geocoding an address
        # from_geocode = gmaps.geocode('東京都台東区上野4丁目4-5')
        # from_location = from_geocode[0]['geometry']['location']
        from_location = {'lat': 35.7085362, 'lng': 139.7734659}

        to_geocode = gmaps.geocode(addr)
        to_location = to_geocode[0]['geometry']['location']

        result = gmaps.directions(from_location, to_location)

        distance = result[0]['legs'][0]['distance']
        return distance['value'] < 1000

    def order_history(self, request, params):
        # get takeout order history by user
        user_id = self.get_user_id(params)
        sql = '''
            SELECT
                *
            FROM
            takeout_order
            WHERE user_id=%(user_id)s
            ORDER BY create_time DESC
        '''
        params = {'user_id': user_id}
        orders = SQL.sql_to_list(sql, params)
        order_ids = []
        map_orders = {}
        for item in orders:
            order_ids.append(item['id'])
            map_orders[item['id']] = item

        sql = '''
            SELECT
                *
            FROM
            takeout_order_detail
            where order_id in %(order_id)s
        '''
        details = SQL.sql_to_list(sql, {'order_id': order_ids})
        for item in details:
            order_id = item['order_id']
            if 'details' not in map_orders[order_id]:
                map_orders[order_id]['details'] = []

            map_orders[order_id]['details'].append(item)

        result = map_orders.values()
        return JsonResponse(result=True, data=result)

    def get_user_id(self, params):
        if 'token' in params:
            r = jwt_decode_handler(params['token'])
            return r['id']
        else:
            return 0

    def get_shop_data(self, request, params):
        '''获取店铺信息数据'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
           *
        FROM master_config
        where key = 'shopinfo'
        '''

        result = SQL.sql_to_list(
            sql=sql, params=sql_param, DB_name=DATA_BASE)

        return JsonResponse(result=True, data=result)
