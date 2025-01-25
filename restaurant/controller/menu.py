import channels.layers
from asgiref.sync import async_to_sync
from django.db import transaction
from rest_framework import authentication, permissions, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

import common.sql as Sql
import master.data.cache_data as cache_data
import common.saas as saas
import xxsubtype
from common.log import logger
from common.permission.controller import UserRoleAuthenticated
from common.util import Util
from common.views.view import SampleAPIView
from common.web.json import JsonResult
from master.models.guest import Guest, GuestUser
from master.models.master import Config
from master.models.menu import (Menu, MenuBind, MenuCourse, MenuCourseDetail,
                                MenuFree, MenuFreeDetail, MenuTop, MenuGift)
from master.models.seat import Seat, SeatStatus
from master.serializer.seat import SeatSerializer, SeatStatusSerializer
import boto3
import web.settings as settings
import base64
import os
import datetime
from app.db.db_patch import SaasHandler


class MenuController(SampleAPIView):
    # 認証
    permission_classes = (UserRoleAuthenticated,)

    # 遅い処理をSQL＋キャッシュ化する
    def menu_list(self, request, *args, **kwargs):

        # menulist = cache_data.get_menu_list()
        # if menulist:
        #     return Response(menulist)

        sql = '''
            SELECT menu.id,
                menu.no,
                menu.name,
                menu.usable,
                menu.price,
                menu.ori_price,
                menu.tax_in,
                menu.note,
                menu.image,
                menu.introduction,
                menu.updated_at,
                menu.stock_status_id AS stock_status,
                master.display_name AS stock_status_name,
                course.level
            FROM MENU
            LEFT JOIN master_data master ON master.id = stock_status_id
            LEFT JOIN menu_course course ON course.menu_id = MENU.id
            WHERE MENU.usable = true
            ORDER BY menu.no ASC
        '''
        menulist = Sql.sql_to_dict(sql)

        result = []
        menu_options = self.get_menu_options()
        menu_course = self.get_menu_course()
        for item in menulist:
            mid = item['id']
            if mid in menu_options:
                item['menu_options'] = menu_options[mid]
            else:
                item['menu_options'] = []
            if item['image'] and item['updated_at']:
                item['image'] = item['image'] + '?' + str(item['updated_at'])

            item['course'] = []
            if mid in menu_course:
                item['course'] = menu_course[mid]
            result.append(item)

        # cache_data.set_menu_list(menulist)
        # print(menulist)
        return Response(result)

    # 遅い処理をSQL＋キャッシュ化する
    def menucategory(self, request, *args, **kwargs):

        sql = '''
        SELECT category_id AS category,
            data_group.id AS category_group,
            data.display_name AS category_name,
            data.display_order,
            category.id AS id,
            menu.id AS menu,
            menu.id AS menu_id,
            menu.no AS menu_no,
            menu.image,
            menu.name AS menu_name,
            menu.price AS menu_price,
            menu.ori_price AS menu_ori_price,
            menu.usable AS menu_usable,
            menu.updated_at AS updated_at,
            menu.stock_status_id AS stock_status,
            menu.note,
            menu.tax_in,
            COALESCE(menu.mincount, 1) AS mincount,
            0 as is_free,
            menu.introduction
        FROM menu_category category
        INNER JOIN menu ON menu.id = category.menu_id
        LEFT JOIN master_data data ON data.id = category.category_id
        LEFT JOIN master_data_group data_group ON data_group.id = data.group_id
        WHERE 1=1
        {0}
        ORDER BY data_group.id, data.id, category.display_order

        '''

        sql_formart = ""
        sql_params = {}
        # cache_key = "ALL"
        if "category_group" in request.GET:
            sql_formart = r" AND data_group.id = %(category_group)s"
            sql_params["category_group"] = request.GET["category_group"]
            # cache_key = request.GET["category_group"]
        sql = sql.format(sql_formart)
        data = Sql.sql_to_dict(sql, sql_params)

        if 'seat_id' in request.GET and "category_group" in request.GET:
            menu_ids = self.getMenuFreeMenuId(
                request.GET['seat_id'], request.GET["category_group"])
            if len(menu_ids) > 0:
                result = []
                for item in data:
                    if item['menu_id'] in menu_ids:
                        item['is_free'] = 1
                        result.append(item)
                data = result

        result = []
        menu_options = self.get_menu_options()
        menu_course = self.get_menu_course()
        for item in data:
            mid = item['menu_id']
            if mid in menu_options:
                item['menu_options'] = menu_options[mid]
            else:
                item['menu_options'] = []
            if item['image'] and item['updated_at']:
                item['image'] = item['image'] + '?' + str(item['updated_at'])

            # process course data
            item['course'] = []
            if mid in menu_course:
                item['course'] = menu_course[mid]
            result.append(item)
        # if cache_data.get_menu_category(cache_key) is None:
            # cache_data.set_menu_category(cache_key, data)

        return Response(result)

    def get_menu_course(self):
        sql = '''
            SELECT
                mc.menu_id,
                mc.id AS course_id,
                mcd.group_id AS group_id,
                menu.*
            FROM menu_course mc
            LEFT JOIN menu_course_detail mcd ON mc.id = mcd.menu_course_id
            LEFT JOIN menu ON mcd.menu_id = menu.id
            ORDER BY mcd.id
        '''
        data = Sql.sql_to_dict(sql)
        result = {}
        for item in data:
            id = item["menu_id"]
            if id not in result:
                result[id] = []
            result[id].append(item)
        return result

    def get_menu_options(self):
        sql = '''
            SELECT
                option.id, option.menu_id,
                coalesce(md.display_name, md.name) AS display_name,
                md.display_order,
                md.group_id,
                coalesce(mdg.display_name, mdg.name) AS group_name, option.price
            FROM menu_option option
            LEFT JOIN master_data md ON option.data_id = md.id
            LEFT JOIN master_data_group mdg ON mdg.id = md.group_id
            ORDER BY md.display_order
        '''
        data = Sql.sql_to_dict(sql)
        result = {}
        for item in data:
            mid = item['menu_id']
            group_id = item['group_id']
            if mid not in result:
                result[mid] = {}
            if group_id not in result[mid]:
                result[mid][group_id] = {
                    'items': [],
                    'group_id': group_id,
                    'group_name': item['group_name']
                }
            result[mid][group_id]['items'].append(item)

        return result

    def getMenuFreeMenuId(self, seat_id, free_type_id):
        params = {
            'seat_id': seat_id,
            'free_type_id': free_type_id
        }

        sql = '''
                SELECT mfd.menu_id FROM order_detail
                    INNER JOIN menu_free ON order_detail.menu_id=menu_free.menu_id
                    INNER JOIN menu_free_detail mfd ON mfd.menu_free_id=menu_free.id
                    INNER JOIN "order" ord ON order_detail.order_id=ord.id AND ord.seat_id=%(seat_id)s
                    INNER JOIN seat_free ON ord.seat_id=seat_free.seat_id AND seat_free.status=1
                    WHERE menu_free.free_type_id = %(free_type_id)s
            '''
        result = Sql.sql_to_dict(sql, params)
        menu_free_id = []
        if len(result):
            for item in result:
                menu_free_id.append(
                    item['menu_id']
                )
        return menu_free_id

        # 遅い処理をSQL＋キャッシュ化する

    def ranking(self, request, *args, **kwargs):
        configs = Config.objects.filter(key='ranking')
        ranking_limit = 15
        ranking_group_ids = (0)
        if len(configs):
            ranking_limit = configs[0].value['limit']
            ranking_group_ids = tuple(configs[0].value['group_id'])

        sql = '''
        SELECT null AS category,
            null AS category_group,
            null AS category_name,
            null as display_order,
            null AS id,
            menu.id AS menu,
            menu.id AS menu_id,
            menu.image AS image,
            menu.no AS menu_no,
            menu.name AS menu_name,
            menu.price AS menu_price,
            menu.ori_price AS menu_ori_price,
            menu.usable AS menu_usable
        FROM (
            select count(1) c, odh.menu_id
                FROM order_detail_history  odh
                INNER JOIN menu_category category ON odh.menu_id=category.menu_id
                INNER JOIN master_data data ON data.id = category.category_id and category.category_id in %(ranking_group_ids)s
                INNER JOIN menu ON odh.menu_id = menu.id AND menu.usable=true
                group by odh.menu_id order by sum(count) desc limit %(ranking_limit)s offset 0
        ) as ranking
        LEFT JOIN menu ON menu.id = ranking.menu_id
        ORDER BY ranking.c desc
        LIMIT %(ranking_limit)s OFFSET 0
        '''

        sql_formart = " "
        sql_params = {
            'ranking_limit': ranking_limit,
            'ranking_group_ids': ranking_group_ids
        }
        print(sql_params)
        cache_key = "ranking" + str(ranking_group_ids) + str(ranking_limit)
        result = None  # cache_data.get_menu_category(cache_key)
        if result is None:
            sql = sql.format(sql_formart)
            data = Sql.sql_to_dict(sql, sql_params)

            result = []
            menu_course = self.get_menu_course()
            menu_options = self.get_menu_options()
            for item in data:
                mid = item['menu_id']

                if mid in menu_options:
                    item['menu_options'] = menu_options[mid]
                else:
                    item['menu_options'] = []

                # process course data
                item['course'] = []
                if mid in menu_course:
                    item['course'] = menu_course[mid]
                result.append(item)

            # cache_data.set_menu_category(cache_key, result)

        return Response(result)

    def init(self, request, *args, **kwargs):
        print(args)
        print(kwargs)

        return Response({'result': True, 'data': {}})

    def menufree_order_detail(self, request, *args, **kwargs):
        '''
        注文済みの放題メニューデータを取得
        放題メニュー注文すす際に、同じ種別複数種類の注文できないように制御のため
        '''
        sql = Sql.get("get_menufree_detail")
        rows = Sql.sql_to_dict(sql, {"seat_id": request.GET["seat_id"]})
        # result = self.to_json()
        return Response(rows)

    def menufree_menus(self, request, *args, **kwargs):
        '''
        テーブル利用可能の食べ放題のすべてのメニューID
        '''
        sql = Sql.get("get_menufree_menus")
        array = Sql.sql_to_list(sql, {"seat_id": request.GET["seat_id"]})
        return Response(array)

    def menufree_time(self, request, *args, **kwargs):
        '''
        テーブル利用可能の食べ放題の種別と開始時間を取得
            注文確認完了時間（利用開始時間）早い方を利用
        '''
        sql = Sql.get("get_menufree_time_byseat")
        rows = Sql.sql_to_dict(sql, {"seat_id": request.GET["seat_id"]})
        return Response(rows)

    def call_staff(self, request, *args, **kwargs):
        seat = request.data
        # print(seat)
        seat["type"] = "call"
        # print(seat)
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            saas.group_name(saas.id(request), '__StaffConsumer__'),
            {
                'type': 'send_message',
                'data': seat
            })

        return Response()

    def end_call(self, request, *args, **kwargs):

        seat = request.data["seat"]
        seat["type"] = "end_call"
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            saas.group_name(saas.id(request), '__StaffConsumer__'),
            {
                'type': 'send_message',
                'data': seat
            })

        return Response()

    def post_menu_top(self, request, *args, **kwargs):
        data = request.data
        obj = MenuTop()
        obj.id = data['id']
        settingpath = SaasHandler.get_saas_id() + '/theme/top1/'
        optionsum = ''
        # 图片列表
        if 'imgData' in data and data['imgData']:
            for i in range(0, len(data['imgName']))[::-1]:
                # name
                imgtime = datetime.datetime.now()
                newimgname = str(imgtime.year) + '' + str(imgtime.month)+'' + str(imgtime.day)+'' + str(
                    imgtime.hour)+'' + str(imgtime.minute)+'' + str(imgtime.microsecond)
                file_name = data['imgName'][i]
                file_name = file_name.replace(
                    file_name.rsplit('.', 1)[0], newimgname)
                filepath = settingpath + file_name
                file_info = data['imgData'][i]
                _, b64data = file_info.split(',')

                s3 = boto3.resource('s3')
                optionsum += filepath + ';'
                if data['imgName1'] == '':
                    obj.image = data['image']

                s3.Bucket('foodlife').put_object(Key=filepath,
                                                 Body=base64.b64decode(b64data), ACL="public-read")
            if data['option'] != None and data['option'] != "":
                optionsum += data['option']
            obj.option = optionsum
        # 図鑑图片
        if 'imgData1' in data and data['imgData1']:
            # name
            file_name = data['imgName1']
            filepath = settingpath + file_name
            file_info = str(data["imgData1"])
            _, b64data = file_info.split(',')

            s3 = boto3.resource('s3')
            obj.image = filepath
            if data['imgData'] == []:
                if 'option' in data:
                    obj.option = data['option']

            s3.Bucket('foodlife').put_object(Key=filepath,
                                             Body=base64.b64decode(b64data), ACL="public-read")
        # 直接点击确认按钮
        if not data['imgData1'] and not data['imgData']:
            if 'option' in data:
                obj.option = data['option']
            if 'image' in data:
                obj.image = data['image']

        if 'link' in data:
            obj.link = data['link']

        if 'name' in data:
            obj.name = data['name']

        obj.target_type = data['target_type']
        obj.save()

        # 对删除的图片进行s3的删除
        if 'dellist' in data and data['dellist']:
            for newdellist in data['dellist']:
                s3 = boto3.resource('s3')
                s3.Bucket('foodlife').delete_objects(
                    Delete={
                        'Objects': [
                           {
                               'Key': newdellist
                           }
                        ]
                    }
                )

        result = {
            'message': '処理しました。'
        }
        return Response(result)

    # menu_top data
    def menu_top(self, request, *args, **kwargs):
        sql = '''
            SELECT *
            FROM menu_top
            ORDER BY sort ASC
        '''
        # cache_key = "menu_top"
        # data = cache_data.get_menu_category(cache_key)
        # if data is None:
        # sql = sql.format(sql_formart)
        data = Sql.sql_to_dict(sql)
        # cache_data.set_menu_category(cache_key, data)

        return Response(data)

    # 遅い処理をSQL＋キャッシュ化する
    def category(self, request, *args, **kwargs):

        sql = '''
        SELECT
            data.id,
            data.display_name
        FROM master_data data
        LEFT JOIN master_data_group data_group ON data_group.id = data.group_id
        {0}
        ORDER BY data.id
        '''

        sql_formart = " "
        sql_params = {}
        # cache_key = "ALL"
        if "category_group" in request.GET:
            sql_formart = r" WHERE data_group.id = %(category_group)s"
            sql_params["category_group"] = request.GET["category_group"]
            # cache_key = request.GET["category_group"]

        # if cache_data.get_menu_category(cache_key) is None:
        sql = sql.format(sql_formart)
        data = Sql.sql_to_dict(sql, sql_params)
        return Response(data)

    def course_list(self, request, *args, **kwargs):
        sql = '''
            SELECT menu.id,
                menu.no,
                menu.name,
                menu.usable,
                menu.price,
                menu.ori_price,
                menu.image,
                menu.tax_in,
                menu.note,
                menu.introduction,
                menu.stock_status_id AS stock_status,
                master.display_name AS stock_status_name,
                menu_course.id AS course_id
            FROM MENU
            INNER JOIN menu_course ON menu.id = menu_course.menu_id
            LEFT JOIN master_data master ON master.id = stock_status_id
            ORDER BY menu_course.id DESC
        '''
        menulist = Sql.sql_to_dict(sql)
        # cache_data.set_menu_list(menulist)
        # print(menulist)
        result = []
        if 'course_detail_menu' in request.data:
            for item in menulist:
                course_id = item['course_id']
                item['course_detail_menu'] = Sql.sql_to_dict(
                    "select menu.id as menu_id, menu.no as menu_no, menu.name as menu_name  from menu_course_detail LEFT JOIN menu ON menu_course_detail.menu_id=menu.id where menu_course_id = %(menu_course_id)s  ORDER BY menu_course_detail.id ASC", {"menu_course_id": course_id})
                result.append(item)
        else:
            result = menulist
        return Response(result)

    def get_course(self, request, *args, **kwargs):
        course_id = request.GET['course_id']
        result = Sql.sql_to_dict('select menu_course.id, menu_course.level, menu.id as menu_id, menu.no, menu.name from menu_course LEFT JOIN menu ON menu_course.menu_id=menu.id where menu_course.id = %(course_id)s ', {
                                 'course_id': course_id})
        if len(result) > 0:
            re = result[0]
            re['menu_course_detail'] = Sql.sql_to_dict(
                "select menu.*,menu_course_detail.group_id  from menu_course_detail LEFT JOIN menu ON menu_course_detail.menu_id=menu.id where menu_course_id = %(menu_course_id)s ORDER BY menu_course_detail.id ASC", {"menu_course_id": course_id})
            result = re
        return Response(result)

    def del_course(self, request, *args, **kwargs):
        data = request.data
        course_id = data['course_id']
        if course_id:
            MenuCourse.objects.filter(id=course_id).delete()
            MenuCourseDetail.objects.filter(menu_course_id=course_id).delete()

        result = {
            'message': '処理しました。',
        }
        return Response(result)

    def post_course(self, request, *args, **kwargs):
        data = request.data
        course_menu_id = data['course_menu_id']

        has = True
        menuCourse = MenuCourse()
        if 'id' in data and data['id'] > 0:
            menuCourse.id = data['id']
            has = len(MenuCourse.objects.filter(
                menu_id=course_menu_id).exclude(id=menuCourse.id)) > 0
        else:
            has = len(MenuCourse.objects.filter(menu_id=course_menu_id)) > 0
        if has:
            result = {
                'message': '存在しました',
                'status': 'failed'
            }
            return Response(result)

        menuCourse.price = 0
        menuCourse.menu_id = course_menu_id
        menuCourse.save()

        # delete current course_menu_id data todo...
        Sql.execute("delete from menu_course_detail where menu_course_id = %(menu_course_id)s ", {
                    "menu_course_id": menuCourse.id})
        menu_introduction = []
        for menu_id in data['course_detail_menu_id']:
            menuCourseDetail = MenuCourseDetail()
            menuCourseDetail.menu_id = menu_id
            menuCourseDetail.menu_course_id = menuCourse.id
            menuCourseDetail.save()
            menu = Menu.objects.get(id=menu_id)
            menu_introduction.append(menu.name)
        menu = Menu.objects.get(id=course_menu_id)
        menu.introduction = "\n".join(menu_introduction)
        menu.save()

        result = {
            'message': '処理しました。',
            'status': 'success',
            'id': menuCourse.id
        }
        return Response(result)

    def save_course(self, request, *args, **kwargs):
        data = request.data
        course_menu_id = data['course_menu_id']

        has = True
        menuCourse = MenuCourse()
        if 'id' in data and data['id'] > 0:
            menuCourse.id = data['id']
            has = len(MenuCourse.objects.filter(
                menu_id=course_menu_id).exclude(id=menuCourse.id)) > 0
        else:
            has = len(MenuCourse.objects.filter(menu_id=course_menu_id)) > 0
        if has:
            result = {
                'message': '存在しました',
                'status': 'failed'
            }
            return Response(result)

        menuCourse.price = 0
        menuCourse.level = data['level']
        menuCourse.menu_id = course_menu_id
        menuCourse.save()

        # delete current course_menu_id data todo...
        Sql.execute("delete from menu_course_detail where menu_course_id = %(menu_course_id)s ", {
                    "menu_course_id": menuCourse.id})
        menu_introduction = []
        for group_id, row in data['course_detail'].items():
            for item in row:
                menuCourseDetail = MenuCourseDetail()
                menuCourseDetail.menu_id = item["id"]
                menuCourseDetail.group_id = group_id
                menuCourseDetail.menu_course_id = menuCourse.id
                menuCourseDetail.save()
                menu_introduction.append(item["name"])
        menu = Menu.objects.get(id=course_menu_id)
        # menu.introduction = "\n".join(menu_introduction)
        menu.save()

        result = {
            'message': '処理しました。',
            'status': 'success',
            'id': menuCourse.id
        }
        return Response(result)

    def free(self, request, *args, **kwargs):
        sql = '''
            SELECT menu_free.*, menu.name as menu_name, master_data_group.display_name as group_name, menu.price as menu_price, menu.tax_in as tax_in
                FROM menu_free
                LEFT JOIN menu ON menu_free.menu_id=menu.id
                LEFT JOIN master_data_group ON menu_free.free_type_id=master_data_group.id
                ORDER BY menu_free.id ASC
        '''
        result = Sql.sql_to_dict(sql)
        for row in result:
            r = Sql.sql_to_dict(
                "SELECT * FROM menu WHERE id=%(menu_id)s", {"menu_id": row['menu_id']})
            if len(r):
                menu = r[0]
                menu['menu_options'] = []
                row['menu'] = menu
        return Response(result)

    def post_free(self, request, *args, **kwargs):
        data = request.data

        menuFree = MenuFree()
        if 'menu_free_id' in data and data['menu_free_id'] > 0:
            menuFree.id = data['menu_free_id']

        menuFree.free_type_id = data['free_type_id']
        menuFree.menu_id = data['menu_id']
        menuFree.save()
        # delete current course_menu_id data todo...
        Sql.execute("delete from menu_free_detail where menu_free_id = %(menu_free_id)s ", {
                    "menu_free_id": menuFree.id})
        for menu_id in data['menu_free_detail']:
            menuFreeDetail = MenuFreeDetail()
            menuFreeDetail.menu_id = menu_id
            menuFreeDetail.menu_free_id = menuFree.id
            menuFreeDetail.save()

        result = {
            'message': '処理しました。',
            'id': menuFree.id
        }
        return Response(result)

    def free_del(self, request, *args, **kwargs):
        menu_free_id = request.data['id']
        if menu_free_id:
            with transaction.atomic():
                Sql.execute("delete from menu_free_detail where menu_free_id = %(menu_free_id)s ", {
                            "menu_free_id": menu_free_id})

                Sql.execute("delete from menu_free where id = %(menu_free_id)s ", {
                            "menu_free_id": menu_free_id})
        result = {
            'message': '処理しました。',
        }
        return Response(result)

    def free_detail(self, request, *args, **kwargs):
        number = request.GET['menu_free_id']
        if request.GET['menu_free_id'] == '':
            number = '0'
        sql = '''
            SELECT
                menu.*
            FROM menu_free_detail mfd
            INNER JOIN menu ON menu.id = mfd.menu_id
            WHERE menu_free_id = %(menu_free_id)s
        '''
        params = {
            'menu_free_id': number
        }
        result = Sql.sql_to_dict(sql, params)
        return Response(result)

    def bind_list(self, request, *args, **kwargs):
        sql = '''
            SELECT
                menu_bind.bind_id, menu_bind.menu_id, menu.name AS menu_name
            FROM menu_bind INNER JOIN menu ON menu_bind.menu_id=menu.id
        '''
        params = {}
        data = Sql.sql_to_dict(sql, params)
        result = {}
        for item in data:
            bind_id = item['bind_id']
            if bind_id not in result:
                result[bind_id] = {
                    'bind_id': bind_id,
                    'menu': []
                }
            result[bind_id]['menu'].append(item)
        return Response(result.values())

    def bind_del(self, request, *args, **kwargs):
        bind_id = request.data['bind_id']
        if bind_id:
            MenuBind.objects.filter(bind_id=bind_id).delete()
        result = {
            'message': '処理しました。',
        }
        return Response(result)

    def post_bind(self, request, *args, **kwargs):
        data = request.data
        result = {}
        if 'menu_ids' in data:
            bind_id = 0
            if 'bind_id' in data and data['bind_id']:
                bind_id = data['bind_id']
            # 事务处理開始
            with transaction.atomic():
                sql = '''SELECT menu_bind.bind_id, menu_bind.menu_id, menu.name AS menu_name
                    FROM menu_bind INNER JOIN menu ON menu_bind.menu_id=menu.id WHERE menu_bind.menu_id in %(menu_ids)s AND bind_id<>%(bind_id)s'''

                re = Sql.sql_to_dict(sql, {'menu_ids': tuple(
                    data['menu_ids']), 'bind_id': bind_id})
                if len(re) > 0:
                    return Response({
                        'message': "[ " + re[0]['menu_name'] + ' ] 存在します'
                    })
                Sql.execute("DELETE FROM menu_bind WHERE menu_id in %(menu_ids)s", {
                            'menu_ids': tuple(data['menu_ids'])})
                Sql.execute("DELETE FROM menu_bind WHERE bind_id = %(bind_id)s", {
                            'bind_id': bind_id})
                for menu_id in data['menu_ids']:
                    if bind_id == 0:
                        bind_id = menu_id
                    MenuBind.objects.create(
                        menu_id=menu_id,
                        bind_id=bind_id
                    )

                result = {
                    'bind_id': bind_id,
                    'message': '処理しました。'
                }
        return Response(result)

    def update_sale_out(self, request, *args, **kwargs):
        data = request.data
        menu = Menu.objects.get(id=data['id'])
        menu.stock_status_id = data['stock_status_id']
        with transaction.atomic():
            menu.save()

        return Response(JsonResult(result=True, message="ステータスが変更しました。"))

    def get_menu_gift_data(self, request, *args, **kwargs):
        data = request.data

        sql_param = {}
        sql_condition = []

        sql = '''
            SELECT
                menu_gift.id,
                menu.name as menu_name,
                menu_gift.use_gift_count,
                menu_gift.flg
            FROM menu_gift
            LEFT JOIN menu ON menu.id = menu_gift.menu_id
            WHERE 1 = 1
            {0}
        '''

        sql_formart = " "
        sql_params = {}
        # cache_key = "ALL"
        if 'keyword' in data and data['keyword']:
            sql_formart = r" AND menu.name LIKE %(keyword)s"
            sql_params["keyword"] = '%' + data["keyword"] + '%'

        sql = sql.format(sql_formart)
        data = Sql.sql_to_dict(sql, sql_params)
        return Response(data)

    def delete_menu_gift(self, request, *args, **kwargs):
        data = request.data
        '''ユーザーデータ削除'''

        menuGift = MenuGift.objects.get(pk=int(data['id']))
        menuGift.delete()

        result = {
            'message': '処理しました。',
        }
        return Response(result)

    def get_menu_gift_edit_data(self, request, *args, **kwargs):
        data = request.data
        sql = '''
            SELECT
                id,
                menu_id,
                use_gift_count,
                flg
            FROM menu_gift
            WHERE
                id = %(id)s
        '''
        params = {
            'id': data['id']
        }
        result = Sql.sql_to_dict(sql, params)
        return Response(result)

    def set_edit_menu_gift_data(self, request, *args, **kwargs):
        data = request.data
        '''ユーザーデータ編集'''

        menuGift = MenuGift.objects.get(pk=data['id'])

        menuGift.menu_id = data['menu_id']
        menuGift.use_gift_count = data['use_gift_count']
        menuGift.flg = data['flg']
        menuGift.save()

        result = {
            'message': '処理しました。',
        }

        return Response(result)

    def save_menu_gift(self, request, *args, **kwargs):
        data = request.data
        menuGift = MenuGift()

        menuGift.menu_id = data['menu_id']
        menuGift.use_gift_count = data['use_gift_count']
        menuGift.flg = data['flg']
        menuGift.save()

        result = {
            'message': '処理しました。',
        }

        return Response(result)
