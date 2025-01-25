
import base64
import os

import numpy
from django.db import transaction
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist

import app.const as Const
import app.common.message as Message
import app.db.sql as SQL
import web.settings as settings
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.exception.web import WebException
from app.db.models.store_table import Menu, MenuCategory, TblRecipe, MasterData, MasterDataGroup, MenuOption
import boto3
import json
from app.db.db_patch import SaasHandler
from master.data.const import SpecialMenu
from master.models.menu import (MenuBind, MenuCourse, MenuCourseDetail,
                                MenuFree, MenuFreeDetail)


class MenuMgmtApi(BaseAPI):

    def get_menu_data(self, request, params):
        '''メニューデータ取得'''

        sql_param = {}
        sql_condition = []

        USE_DATABASE = 'ami'

        sql = '''
        SELECT
            mst.id,
            mst.no,
            mst.name,
            mst.usable,
            mst.price || '円' AS price,
            mst.note,
            mst.introduction,
            mst.tax_in,
            mst.takeout,
            mst.mincount,
            mst.updated_at
        FROM
            menu mst
            LEFT JOIN menu_category cat ON cat.menu_id = mst.id
        WHERE 1 = 1 and mst.no not in %(specialmenu)s
            {0}
		GROUP BY
			mst.id
        ORDER BY
            mst.no
        '''

        sql_param['specialmenu'] = [
            SpecialMenu.Other_tax_none,
            SpecialMenu.Other_tax_in
        ]
        if 'keyword' in params and params['keyword']:
            sql_condition.append(
                ' AND mst.name LIKE %(keyword)s'
            )
            sql_param['keyword'] = '%' + params['keyword'] + '%'

        if 'filter' in params and params['filter']:
            sql_condition.append(' AND cat.category_id in %(filter)s')
            sql_param['filter'] = params['filter']

        sql = sql.format('\n'.join(sql_condition))
        menu_list = SQL.sql_to_list(
            sql=sql, params=sql_param, DB_name=USE_DATABASE)

        category = self.get_menu_cat()
        menu_cat = []
        for cat in category:
            for child in cat['children']:
                child['display_name'] = cat['display_name'] + \
                    '／' + child['display_name']
                menu_cat.append(child)

        data = {
            'menu': menu_list,
            'filter_cat': self.get_menu_cat(),
            'category': menu_cat,
            'site_image_host': settings.SITE_IMAGE_HOST,
            'desabled_delete_menu_no': [
                SpecialMenu.Other_tax_none,
                SpecialMenu.Other_tax_in,
                SpecialMenu.Table_charge
            ]
        }
        return JsonResponse(result=True, data=data)

    def set_menu_data(self, request, params):
        '''メニュー保存'''
        USE_DATABASE = 'ami'

        # メニュー画像設定
        default_size = int(settings.LIMIT_SIZE) * 1024
        default_path = settings.STATIC_ROOT

        with transaction.atomic(using=USE_DATABASE):
            try:
                # old_menu_cats = []
                # old_recipes = []
                if 'ori_price' not in params or not params['ori_price']:
                    params['ori_price'] = 0
                    
                if 'menu_id' in params and params['menu_id']:
                    menu = Menu.objects.using(USE_DATABASE).get(id=params['menu_id'])
                    # menus = SQL.sql_to_list("select * from menu where id=%(id)s", {"id": params['menu_id']})
                    # menu = Menu()
                    # menu.setValues(menus[0])
                    # print(menu.__dict__)
                    menu.save(request=request, values=params,
                              using=USE_DATABASE)
                    # 関連するカテゴリーとレシピを取得
                    # old_menu_cats = MenuCategory.objects.using(
                    #     USE_DATABASE).filter(menu_id=params['menu_id'])
                    # old_recipes = TblRecipe.objects.using(
                    #     USE_DATABASE).filter(menu_id=params['menu_id'])
                    # old_menu_cats = params['menu_category_id']
                    # old_recipes = params['menu_option_id']
                else:
                    menu = Menu()
                    menu.no = self.get_menu_no()
                    menu.insert(request=request, values=params,
                                using=USE_DATABASE)

                menu_id = menu.id
                # 関連してるカテゴリーとレシピの保存
                cat = MenuCategory.objects.filter(menu_id=menu_id)
                exclude_id = []
                if 'menu_category' in params and params['menu_category']:
                    for row in params['menu_category']:
                        menuCatObj = MenuCategory()
                        menuCatObj.menu_id = menu_id
                        menuCatObj.category_id = row
                        menuCatObj.display_order = 0
                        for item in cat:
                            if item.category_id == row:
                                menuCatObj.id = item.id
                                menuCatObj.display_order = item.display_order
                                break
                        menuCatObj.save()
                        exclude_id.append(menuCatObj.id)
                MenuCategory.objects.filter(menu_id=menu_id).exclude(id__in=exclude_id).delete()

                opt = MenuOption.objects.filter(menu_id=menu_id)
                exclude_id = []
                if 'menu_option' in params and params['menu_option']:
                    for row in params['menu_option']:
                        menu_option_price = 0
                        if 'menu_option_price' in params and params['menu_option_price']:
                            for item in params['menu_option_price']:
                                if item['id']==row:
                                    menu_option_price = item['price']
                        menuOptObj = MenuOption()
                        menuOptObj.menu_id = menu_id
                        menuOptObj.data_id = row
                        menuOptObj.display_order = 0
                        menuOptObj.price = menu_option_price

                        for item in opt:
                            if item.data_id == row:
                                menuOptObj.id = item.id
                                menuOptObj.display_order = item.display_order
                        menuOptObj.save()
                        exclude_id.append(menuOptObj.id)
                MenuOption.objects.filter(menu_id=menu_id).exclude(id__in=exclude_id).delete()

                
                rec_old = TblRecipe.objects.filter(menu_id=menu_id)
                if 'recipe' in params and params['recipe']:
                    for row in params['recipe']:
                        if 'ing_id' in row and row['ing_id']:
                            rec = TblRecipe.objects.filter(ing_id=row['ing_id'],menu_id=menu_id)
                            if len(rec) == 1:
                                for r in rec:
                                    r.menu_id = menu_id
                                    r.save(request=request,
                                          values=row, using=USE_DATABASE)
                                    rec_old = rec_old.exclude(id=r.id)
                            elif len(rec) > 1:
                                for r in rec:
                                    r.delete()
                                    rec_old = rec_old.exclude(id=r.id)
                                recipe = TblRecipe()
                                recipe.menu_id = menu_id
                                recipe.insert(request=request,
                                            values=row, using=USE_DATABASE)
                            else:
                                recipe = TblRecipe()
                                recipe.menu_id = menu_id
                                recipe.insert(request=request,
                                            values=row, using=USE_DATABASE)
                # レシピ削除
                if len(rec_old) != 0:
                    for old in rec_old:
                        old.delete()

                # メニュー画像保存
                if "imgData" in params and params["imgData"]:
                    file_name = '/menu_images/' + str(menu.no) + '.jpg'
                    file_size = params["size"] if "size" in params else 0

                    # ファイル作成
                    file_info = str(params["imgData"])
                    _, b64data = file_info.split(',')

                    s3 = boto3.resource('s3')
                    image_url = SaasHandler.get_saas_id() + file_name
                    s3.Bucket('foodlife').put_object(
                        Key=image_url, Body=base64.b64decode(b64data), ACL="public-read")
                    menu.image = image_url
                    menu.save()


            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005), data=menu_id)
    
    def get_menu_no(self):
        print("---get_menu_no----")
        result = Menu.objects.aggregate(Max('no'))
        print("---get_menu_no----end--------")
        max = 0
        if 'no__max' in result:
            max = result['no__max']
        if max==None:
            max = 0
        max = max + 1
        return max

    def get_menu_detail(self, request, params):
        '''メニュー詳細データ'''
        result = []
        USE_DATABASE = 'ami'
        if 'menu_id' in params and params['menu_id']:
            sql = '''
            SELECT
                menu.id AS menu_id,
                menu.no,
                menu.name,
                menu.usable,
                menu.price,
                menu.introduction,
                menu.tax_in,
                menu.ori_price,
                menu.takeout,
                COALESCE(menu.mincount, 1) AS mincount,
                menu.image,
                menu.stock_status_id
            FROM
                menu
            WHERE menu.id = %(menu_id)s
            '''
            result = SQL.sql_to_list(
                sql=sql, params={'menu_id': params['menu_id']}, DB_name=USE_DATABASE)

            if result:
                sql = '''
                SELECT
                    string_to_array(
                        string_agg(
                        distinct cat.category_id ::text
                        , ',')
                        , ','
                    ) AS menu_category,
                    string_to_array(
                        string_agg(
                        distinct cat.id ::text
                        , ',')
                        , ','
                    ) AS menu_category_id
                FROM
                    (select id, category_id, menu_id from menu_category WHERE menu_id = %(menu_id)s order by id) as cat
                '''
                cat_result = SQL.sql_to_list(
                    sql=sql, params={'menu_id': params['menu_id']}, DB_name=USE_DATABASE)

                if cat_result:
                    # メニューカテゴリーを数字リスト形式にする
                    if cat_result[0]['menu_category']:
                        cat_result[0]['menu_category'] = [
                            int(i) for i in cat_result[0]['menu_category']]
                    if cat_result[0]['menu_category_id']:
                        cat_result[0]['menu_category_id'] = [
                            int(i) for i in cat_result[0]['menu_category_id']]

                result[0]['menu_category'] = cat_result[0]['menu_category']
                result[0]['menu_category_id'] = cat_result[0]['menu_category_id']

                # sql = '''
                # SELECT
                #     string_to_array(
                #         string_agg(
                #         distinct opt.data_id ::text
                #         , ',')
                #         , ','
                #     ) AS menu_option,
                #     string_to_array(
                #         string_agg(
                #         distinct opt.id ::text
                #         , ',')
                #         , ','
                #     ) AS menu_option_id,
                #     string_to_array(
                #         string_agg(
                #         distinct opt.price ::text
                #         , ',')
                #         , ','
                #     ) AS menu_option_price
                # FROM
                #     (select id, data_id, menu_id, price from menu_option WHERE menu_id = %(menu_id)s order by id) as opt
                # '''
                # opt_result = SQL.sql_to_list(
                #     sql=sql, params={'menu_id': params['menu_id']}, DB_name=USE_DATABASE)

                # if opt_result:
                #     if opt_result[0]['menu_option']:
                #         opt_result[0]['menu_option'] = [
                #             int(i) for i in opt_result[0]['menu_option']]
                #     if opt_result[0]['menu_option_id']:
                #         opt_result[0]['menu_option_id'] = [
                #             int(i) for i in opt_result[0]['menu_option_id']]
                #     if opt_result[0]['menu_option_price']:
                #         opt_result[0]['menu_option_price'] = [
                #             int(i) for i in opt_result[0]['menu_option_price']]

                # result[0]['menu_option'] = opt_result[0]['menu_option']
                # result[0]['menu_option_id'] = opt_result[0]['menu_option_id']
                # result[0]['menu_option_price'] = opt_result[0]['menu_option_price']
                sql ="select id, data_id, menu_id, price from menu_option WHERE menu_id = %(menu_id)s order by id"
                opt_result = SQL.sql_to_list(
                    sql=sql, params={'menu_id': params['menu_id']}, DB_name=USE_DATABASE)
                result[0]['menu_option'] = []
                result[0]['menu_option_id'] = []
                result[0]['menu_option_price'] = []
                for row in opt_result:
                    result[0]['menu_option'].append(row['data_id'])
                    result[0]['menu_option_id'].append(row['id'])
                    result[0]['menu_option_price'].append(row['price'])

                # 関連レシピを取得
                recipe_sql = '''
                SELECT
                    ing_id,
                    serving,
                    amount_to_use,
                    stock_unit,
                    consumption_unit,
                    unit_conv_rate,
                    ave_price,
                    (ave_price * amount_to_use) as recipe_cost
                FROM
                    tbl_recipe        rec
                LEFT JOIN mst_ingredients   ing ON rec.ing_id = ing.id
                WHERE
                    rec.menu_id = %(menu_id)s
                '''

                recipe = SQL.sql_to_list(sql=recipe_sql, params={
                                        'menu_id': result[0]['menu_id']}, DB_name=USE_DATABASE)
                result[0]['recipe'] = recipe

                # メニュー画像データ取得
                # img_path = settings.STATIC_ROOT + result[0]['image']

                # if result[0]['image'] and os.path.exists(img_path):
                #     with open((img_path), "rb") as file_info:
                #         data_info = file_info.read()
                #     result[0]["img_data"] = base64.b64encode(data_info)
                # else:
                #     result[0]["img_data"] = None

        ing_sql = '''
        SELECT
            id AS ing_id,
            ing_no,
            ing_name,
            stock_unit,
            consumption_unit,
            unit_conv_rate,
            ave_price
        FROM
            mst_ingredients
        '''
        ing_list = SQL.sql_to_list(ing_sql, DB_name=USE_DATABASE)
        data = {
            'result': result[0] if result else {},
            'ing': ing_list,
            'menu_cat': self.get_menu_cat(),
            'menu_option': self.get_menu_option(),
            'site_image_host': settings.SITE_IMAGE_HOST
        }
        return JsonResponse(result=True, data=data)

    def get_menu_cat(self, kitchen='all'):
        '''メニューカテゴリー取得'''

        USE_DATABASE = 'ami'

        parent_sql = '''
        SELECT
            id,
            coalesce(display_name, name) AS display_name,
            display_order,
            option
        FROM
            master_data_group
        WHERE
            domain = 'menu_category'
        '''
        if kitchen!='all':
            if kitchen:
                parent_sql = parent_sql + " AND name='menu_category_standard'"
            else:
                parent_sql = parent_sql + " AND name!='menu_category_standard'"
        parent_sql = parent_sql + ' ORDER BY display_order, id ASC'
            
        parents = SQL.sql_to_list(parent_sql, DB_name=USE_DATABASE)
        parents.sort(key=lambda x: (
            x['display_order'] is None, x['display_order']))

        children_sql = '''
        SELECT
		    code,
            coalesce(display_name, name) AS display_name,
		    theme_id,
		    menu_count,
            display_order,
            id,
            group_id
        FROM
            master_data
        WHERE
            group_id IN %(group_id)s
        ORDER BY display_order, id ASC
        '''
        group_list = [p['id'] for p in parents]
        children = SQL.sql_to_list(sql=children_sql, params={
                                   'group_id': group_list}, DB_name=USE_DATABASE)

        for parent in parents:
            parent['children'] = []
            parent['display'] = 'none'
            
            parent = self.parse_option(parent)

            for child in children:
                if child['group_id'] == parent['id']:
                    child['parent_name'] = parent['display_name']
                    parent['children'].append(child)
            parent['children'].sort(key=lambda x: (
                x['display_order'] is None, x['display_order']))

        return parents

    def parse_option(self, data):
        data['option_img'] = ''
        data['option_display'] = True
        if 'option' in data and data['option']:
            for key in data['option']:
                new_key = 'option_' + key
                data[new_key] = data['option'][key]
        data['site_image_host'] = settings.SITE_IMAGE_HOST
        return data

    def delete_menu_data(self, request, params):
        '''メニューデータ削除'''

        USE_DATABASE = 'ami'

        for row in params['rows']:
            if row["no"]==SpecialMenu.Table_charge:
                return JsonResponse(result=False, message='メユー「お通し」削除できません。')

            Menu.objects.using(USE_DATABASE).get(id=row['id']).delete()
            MenuCategory.objects.using(USE_DATABASE).filter(menu_id=row['id']).delete()
            TblRecipe.objects.using(USE_DATABASE).filter(menu_id=row['id']).delete()

            MenuBind.objects.filter(menu_id=row['id']).delete()
            MenuCourse.objects.filter(menu_id=row['id']).delete()
            MenuCourseDetail.objects.filter(menu_id=row['id']).delete()
            MenuFree.objects.filter(menu_id=row['id']).delete()
            MenuFreeDetail.objects.filter(menu_id=row['id']).delete()

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def move_menu(self, request, params):
        '''メニュー移動'''

        USE_DATABASE = 'ami'

        with transaction.atomic(using=USE_DATABASE):
            try:
                if 'rows' in params and params['rows']:
                    for row in params['rows']:
                        old_menu_cats = []
                        if 'id' in row and row['id']:
                            old_menu_cats = MenuCategory.objects.using(
                                USE_DATABASE).filter(menu_id=row['id'])

                        # 保存前に関連してるカテゴリーとレシピ削除
                        if old_menu_cats:
                            for cat in old_menu_cats:
                                cat.delete()

                        # 選択されたカテゴリー保存
                        for cat in params['menu_category']:
                            new_cat = MenuCategory()
                            new_cat.menu_id = row['id']
                            new_cat.category_id = cat
                            new_cat.display_order = 0
                            new_cat.insert(using=USE_DATABASE)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_cat_data(self, request, params):
        '''メニューカテゴリー一覧を取得'''

        cats = self.get_menu_cat(params['kitchen'])

        return JsonResponse(result=True, data=cats)

    def update_cat_data(self, request, params):
        '''メニューカテゴリー更新'''

        USE_DATABASE = 'ami'

        parents = []
        children = []

        if 'parents' in params and params['parents']:
            parents = params['parents']
        if 'children' in params and params['children']:
            children = params['children']

        with transaction.atomic(using=USE_DATABASE):
            try:
                for row in parents:
                    parent = MasterDataGroup.objects.using(
                        USE_DATABASE).get(id=row['id'])
                    parent.save(request=request, values=row,
                                using=USE_DATABASE)
                for row in children:
                    child = MasterData.objects.using(
                        USE_DATABASE).get(id=row['id'])
                    child.save(request=request, values=row, using=USE_DATABASE)
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def add_cat_data(self, request, params):
        '''メニューカテゴリー追加'''

        USE_DATABASE = 'ami'

        with transaction.atomic(using=USE_DATABASE):
            try:
                if 'group_id' in params and params['group_id']:
                    children = MasterData.objects.using(USE_DATABASE).filter(
                        group_id=int(params['group_id']))
                    max_code = children.aggregate(
                        Max('code'))['code__max'] or 0
                    child = MasterData()
                    child.code = max_code + 1
                    child.name = params['display_name']
                    child.theme_id = 'default'
                    child.menu_count = 9
                    child.insert(request=request, values=params,
                                 using=USE_DATABASE)

                else:
                    parent = MasterDataGroup()
                    parent.name = params['display_name']
                    parent.domain = 'menu_category'
                    parent.note = 'メニュー'
                    parent.enabled = 1
                    parent.option = {
                        'display': False
                    }
                    parent.insert(request=request, values=params,
                                  using=USE_DATABASE)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def delete_cat_data(self, request, params):
        '''メニューカテゴリー追加'''

        USE_DATABASE = 'ami'

        with transaction.atomic(using=USE_DATABASE):
            try:
                if 'rows' in params and params['rows']:
                    for row in params['rows']:
                        if 'group_id' in row and row['group_id']:
                            children = MasterData.objects.using(
                                USE_DATABASE).get(id=int(row['id']))
                            children.delete()

                        elif 'group_id' not in row:
                            parent = MasterDataGroup.objects.using(
                                USE_DATABASE).get(id=int(row['id']))
                            parent.delete()

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def move_cat_group(self, request, params):
        '''メニューカテゴリー移動'''

        USE_DATABASE = 'ami'

        with transaction.atomic(using=USE_DATABASE):
            try:
                if 'rows' in params and params['rows']:
                    for row in params['rows']:
                        if 'group_id' in row and row['group_id']:
                            children = MasterData.objects.using(
                                USE_DATABASE).get(id=int(row['id']))
                            children.group_id = params['group_id']
                            children.save(request=request, using=USE_DATABASE)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_course_data(self, request, params):
        '''コースデータ取得'''

        sql = '''
        SELECT
            menu.id,
            menu.name,
            course.display_order,
            string_to_array(string_agg(det.menu_id ::text, ',' order by menu.no), ',') AS menu_category
        FROM
            menu_course          course
            LEFT JOIN menu_course_detail   det ON det.menu_course_id = course.id
            LEFT JOIN menu ON menu.id = course.menu_id
        GROUP BY
            course.id,
            menu.name,
            menu.id
        order by course.display_order
        '''

        result = SQL.sql_to_list(sql=sql)

        if result:
            for row in result:
                # メニュー画像データ取得
                img_path = settings.STATIC_ROOT + row['image']

                if row['image'] and os.path.exists(img_path):
                    with open((img_path), "rb") as file_info:
                        data_info = file_info.read()
                    row["img_data"] = base64.b64encode(data_info)
                else:
                    row["img_data"] = None

        return JsonResponse(result=True, data=result)

    def get_menu_option(self):
        '''メニューカテゴリー取得'''

        USE_DATABASE = 'ami'

        parent_sql = '''
        SELECT
            id,
            coalesce(display_name, name) AS display_name,
            display_order
        FROM
            master_data_group
        WHERE
            domain = 'menu_option'
        '''
        parents = SQL.sql_to_list(parent_sql, DB_name=USE_DATABASE)
        parents.sort(key=lambda x: (
            x['display_order'] is None, x['display_order']))

        children_sql = '''
        SELECT
            id,
            group_id,
            coalesce(display_name, name) AS display_name,
            display_order
        FROM
            master_data
        WHERE
            group_id IN %(group_id)s
        '''
        group_list = [p['id'] for p in parents]
        children = []
        if len(group_list) > 0:
            children = SQL.sql_to_list(sql=children_sql, params={
                                       'group_id': group_list}, DB_name=USE_DATABASE)

        for parent in parents:
            parent['children'] = []
            parent['display'] = 'none'
            for child in children:
                if child['group_id'] == parent['id']:
                    child['parent_name'] = parent['display_name']
                    parent['children'].append(child)
            parent['children'].sort(key=lambda x: (
                x['display_order'] is None, x['display_order']))

        return parents

    def get_option_data(self, request, params):
        '''メニューカテゴリー一覧を取得'''

        options = self.get_menu_option()

        return JsonResponse(result=True, data=options)

    def update_option_data(self, request, params):
        '''メニューカテゴリー更新'''

        USE_DATABASE = 'ami'

        parents = []
        children = []

        if 'parents' in params and params['parents']:
            parents = params['parents']
        if 'children' in params and params['children']:
            children = params['children']

        with transaction.atomic(using=USE_DATABASE):
            try:
                for row in parents:
                    parent = MasterDataGroup.objects.using(
                        USE_DATABASE).get(id=row['id'])
                    parent.save(request=request, values=row,
                                using=USE_DATABASE)
                for row in children:
                    child = MasterData.objects.using(
                        USE_DATABASE).get(id=row['id'])
                    child.save(request=request, values=row, using=USE_DATABASE)
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def add_option_data(self, request, params):
        '''メニューカテゴリー追加'''

        USE_DATABASE = 'ami'

        with transaction.atomic(using=USE_DATABASE):
            try:
                if 'group_id' in params and params['group_id']:
                    children = MasterData.objects.using(USE_DATABASE).filter(
                        group_id=int(params['group_id']))
                    max_code = children.aggregate(
                        Max('code'))['code__max'] or 0
                    child = MasterData()
                    child.code = max_code + 1
                    child.name = params['display_name']
                    child.theme_id = 'default'
                    child.menu_count = 9
                    child.insert(request=request, values=params,
                                 using=USE_DATABASE)

                else:
                    parent = MasterDataGroup()
                    parent.name = params['display_name']
                    parent.domain = 'menu_option'
                    parent.note = 'メニュー'
                    parent.enabled = 1
                    parent.insert(request=request, values=params,
                                  using=USE_DATABASE)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def delete_option_data(self, request, params):
        '''メニューカテゴリー追加'''

        USE_DATABASE = 'ami'

        with transaction.atomic(using=USE_DATABASE):
            try:
                if 'rows' in params and params['rows']:
                    for row in params['rows']:
                        if 'group_id' in row and row['group_id']:
                            children = MasterData.objects.using(
                                USE_DATABASE).get(id=int(row['id']))
                            children.delete()

                        elif 'group_id' not in row:
                            parent = MasterDataGroup.objects.using(
                                USE_DATABASE).get(id=int(row['id']))
                            parent.delete()

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def move_option_group(self, request, params):
        '''メニューカテゴリー移動'''

        USE_DATABASE = 'ami'

        with transaction.atomic(using=USE_DATABASE):
            try:
                if 'rows' in params and params['rows']:
                    for row in params['rows']:
                        if 'group_id' in row and row['group_id']:
                            children = MasterData.objects.using(
                                USE_DATABASE).get(id=int(row['id']))
                            children.group_id = params['group_id']
                            children.save(request=request, using=USE_DATABASE)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def select_parent_data(self, request, params):
        '''カテゴリー親の修正情報'''
        USE_DATABASE = 'ami'
        parent_sql = '''
        SELECT
            id,
            coalesce(display_name, name) AS display_name,
            option,
            display_order
        FROM
            master_data_group
        WHERE
            domain = 'menu_category'
        AND
            id = %(id)s
        '''

        result = SQL.sql_to_list(
            parent_sql, params={'id': params['parent_id']}, DB_name=USE_DATABASE)
        
        data = {}
        if len(result):
            data = result[0]
            data = self.parse_option(data)

        return JsonResponse(result=True, data=data)

    def select_child_data(self, request, params):
        '''カテゴリー子の修正情報'''
        USE_DATABASE = 'ami'
        parent_sql = '''
        SELECT
		    code,
            coalesce(display_name, name) AS display_name,
		    theme_id,
		    menu_count,
            display_order,
            id,
            group_id,
            option
        FROM
            master_data
        WHERE 
            id = %(id)s
        '''

        result = SQL.sql_to_list(
            parent_sql, params={'id': params['parent_id']}, DB_name=USE_DATABASE)
            
        data = {}
        if len(result):
            data = result[0]
            data = self.parse_option(data)

        return JsonResponse(result=True, data=result)

    def select_option_data(self, request, params):
        '''オプションカテゴリーの修正情報'''
        USE_DATABASE = 'ami'
        parent_sql = '''
        SELECT
            id,
            coalesce(display_name, name) AS display_name,
            display_order
        FROM
            master_data_group
        WHERE
            domain = 'menu_option'
        AND
            id = %(id)s
        '''

        result = SQL.sql_to_list(
            parent_sql, params={'id': params['parent_id']}, DB_name=USE_DATABASE)

        return JsonResponse(result=True, data=result)

    def select_option_child_data(self, request, params):
        '''オプションカテゴリー子の修正情報'''
        USE_DATABASE = 'ami'
        parent_sql = '''
        SELECT
		    id,
            coalesce(display_name, name) AS display_name,
            display_order
        FROM
            master_data
        WHERE 
            id = %(id)s
        '''

        result = SQL.sql_to_list(
            parent_sql, params={'id': params['parent_id']}, DB_name=USE_DATABASE)

        return JsonResponse(result=True, data=result)

    def update_data(self, request, params):
        '''メニューカテゴリー更新'''

        USE_DATABASE = 'ami'
        option = {}
        for key in params:
            if len(key)>7 and key[0:7]=='option_':
                new_key = key[7:]
                option[new_key] = params[key]
        
        params['option'] = option

        if(params['flag'] == "parent"):
            parent = MasterDataGroup.objects.using(
                USE_DATABASE).get(id=params['id'])
            if 'show_time' in params:
                params['option']['show_time'] = params['show_time']
            parent.save(request=request, values=params, using=USE_DATABASE)
        if(params['flag'] == "child"):
            # メニュー画像保存
            if "photo_args" in params and params["photo_args"]:
                photo_args = []
                for row in params['photo_args']:
                    file_name = "/theme/menucat/{0}/{1}.jpg".format(params['id'], (len(photo_args) + 1))
                    file_size = row["size"] if "size" in row else 0

                    # ファイル作成
                    file_info = str(row["imgData"])
                    _, b64data = file_info.split(',')

                    s3 = boto3.resource('s3')
                    image_url = SaasHandler.get_saas_id() + file_name
                    s3.Bucket('foodlife').put_object(Key=image_url, Body=base64.b64decode(b64data), ACL="public-read")
                    photo_args.append(image_url)
                params['option']['photo_args'] = photo_args
            parent = MasterData.objects.using(
                USE_DATABASE).get(id=params['id'])
            parent.save(request=request, values=params, using=USE_DATABASE)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))
