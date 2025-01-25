
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from urllib3 import request

import app.common.message as Message
import app.const as Const
import app.db.sql as SQL
from app.auth.backend import WebException
from app.db.models.tbl import TblInspection
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.models import MstUser
from app.db.models.store_table import MstIngredients, MstIngredientsCat, MenuCategory
import xlwt
import openpyxl as px
from io import BytesIO
from django.http import HttpResponse
from app.db.models.mst import MstStock
from app.db.models.store_table import ProfitInventory,ProfitInventoryDetail
import datetime

class S03p01Api(BaseAPI):

    # 検索ボタン押下
    def get_inventorycontrol_data(self, request, params):

        result = self.get_data_info(params, request.user)
        return JsonResponse(result=True, data=result)

    # 棚卸一覧 ダウンロードボタン押下
    def export_inventorycontrol_data(self, request, params):
        head = ['部品種類','材料名','部品実際在庫数量','棚卸数','備考' ]
        data = self.get_data_info(params, request.user)
        filename = 'export'
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        for i in range(0, len(head)):
            sheet.write(0, i, head[i])
        for row in range(1, len(data) + 1):
            for col in range(0, len(data[0].items())):
                itemName = list(data[row - 1].keys())[col]
                if itemName == 'id' or itemName == 'part_id' or itemName == 'part_type' or itemName == 'rownum' or itemName == 'ave_price':
                    continue
                sheet.write(row, col-4, u'%s' % list(data[row - 1].values())[col])
        workbook.save(r"%s.xls" % filename)
        sio = BytesIO()  # StringIO用来作为字符串的缓存，有些接口和文件操作一致，代码可以同时当成文件操作或者StringIO操作。
        workbook.save(sio) 
        sio.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % filename

        #xlsx文件，出现拓展名的地方都要改为xlsx
        # response = HttpResponse(sio.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename

        response.write(sio.getvalue())
        # exist_file = os.path.exists(r"%s.xls" % filename)    
        # if exist_file:    #生成的文件会在项目文件里存留，所以在下载或者发送之后要删除
        #     os.remove(r"%s.xls" % filename)
        return response

    # 棚卸一覧 保存ボタン押下
    def save_inventory_actual(self, request, params):
        with transaction.atomic():
            try:
                actual_date = datetime.datetime.strptime(params['actual_date'] + ' 09:00:00', '%Y/%m/%d %H:%M:%S') 
                #actual_date = actual_date.strftime("%Y-%m-%d %H:%M:%S")
                parts_inventory_actual_edit = params['parts_inventory_actual_edit']
                remarks_edit = params['remarks_edit']
                inventory_user = params['inventory_user'] 
                dataSource = params['dataSource']
                
                # 棚卸管理テーブルに新規
                profitInventory = ProfitInventory()
                profitInventory.inventory_date = actual_date
                profitInventory.inventory_user = inventory_user
                profitInventory.status = 0
                profitInventory.save()

                inventory_id = profitInventory.pk
                index = 0
                for item in dataSource:
                    id = item['id']
                    mstStock = MstStock.objects.get(id=id)
                    mstStock.parts_inventory_actual = parts_inventory_actual_edit[index]
                    mstStock.save()
                    
                    if item['part_type']==2:
                        index = index + 1
                        continue
                    
                    print(actual_date)
                    # 棚卸管理明細テーブルに新規
                    profitInventoryDetail = ProfitInventoryDetail(inventory_date=actual_date,part_id=item['part_id'])
                    profitInventoryDetail.inventory_id = inventory_id
                    profitInventoryDetail.inventory_date = actual_date
                    profitInventoryDetail.part_id = item['part_id']
                    profitInventoryDetail.parts_type = item['parts_type']
                    profitInventoryDetail.part_name = item['part_name']
                    profitInventoryDetail.parts_inventory_qty = item['parts_inventory_qty']
                    profitInventoryDetail.parts_inventory_actual = parts_inventory_actual_edit[index]
                    profitInventoryDetail.ave_price = item['ave_price']
                    profitInventoryDetail.remarks = remarks_edit[index]
                    profitInventoryDetail.save()
                    index = index + 1

                
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00023)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_data_info(self, request_param, user):
        # print(request_param)
        sql_condition = []
        sql_param = {}

        sql = '''
            SELECT
                row_number() OVER() as rownum,
                sto.id,
                sto.part_id,
                sto.part_type,
                ing.ing_name part_name,
                cat.cat_name parts_type,
                sto.parts_inventory_qty,
                sto.parts_inventory_actual,
                ing.ave_price,
                sto.remarks
            FROM
                mst_stock       sto
            LEFT JOIN
                mst_ingredients      ing
            ON
                sto.part_id = ing.id
            LEFT JOIN
                mst_ingredients_cat  cat
            ON
                ing.ing_cat_id = cat.id
            WHERE 1 = 1
                {0}
            ORDER BY
                sto.id
            '''
        
        if "part_name" in request_param and request_param["part_name"]:
            sql_condition.append("AND ing.ing_name LIKE %(part_name)s")
            sql_param["part_name"] = "%" + request_param["part_name"] + "%"

        if "parts_type" in request_param and request_param["parts_type"]:
            sql_condition.append("AND cat.cat_name LIKE %(parts_type)s")
            sql_param["parts_type"] = "%" + request_param["parts_type"] + "%"

        
        if 'type' in request_param:
            if request_param["is_menu"] == 1:
                if request_param["type"]:
                    sql_condition.append(" AND cat.id in %(type)s")
                    sql_param["type"] = request_param["type"]  
            else:
                if request_param["type"]:
                    sql_condition.append(" AND (cat.id in %(type)s or sto.part_type = 2)")
                    sql_param["type"] = request_param["type"]
                else:
                    sql_condition.append(" AND sto.part_type = 2")
        

        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_list(sql=sql, params=sql_param)
        
        sql = '''
            SELECT
                menu.id,
                menu.name
            FROM mst_stock sto 
            INNER JOIN menu on sto.part_id = menu.id
            WHERE sto.part_type = 2
            '''
        result_menu = SQL.sql_to_list(sql=sql, params=sql_param)
        map_menu = {}
        for item in result_menu:
            map_menu[item['id']] = item['name']
        for item in result:
            if item['part_type']==2:
                if item['part_id'] in map_menu:
                    item['part_name'] = map_menu[item['part_id']]
                    item['parts_type'] = 'メニュー'
        return result

    # 点検データ取得する
    def get_check_info(self, request, params):

        check_info_result = self.get_check_info_data()
        cat_list = self.get_cat_list()

        data = {
            'rows': check_info_result,
            'categories': cat_list
        }

        return JsonResponse(result=True, data=data)

    def get_check_info_data(self):

        # 検索リストデ－タ取得

        sql = '''
        SELECT
            mst.id,
            mst.part_name,
            mst.parts_type,
            mst.part_unit
        FROM
            mst_parts mst
            inner join mst_stock on mst.id = mst_stock.part_id
        ORDER BY
            mst.part_code
        '''

        result = SQL.sql_to_list(sql=sql)

        return result

    # 点検保存ボタン押下

    def save_click(self, request, params):
        with transaction.atomic():
            try: 
                inspection = TblInspection()
                inspection.insert(values=params, request=request)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00023)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_ing_data(self, request, params):
        '''材料データ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            ing.id,
            ing.ing_name
        FROM
            mst_ingredients       ing
        WHERE 1 = 1
            {0}
        ORDER BY
            ing.ing_no
        '''

        if 'keyword' in params and params['keyword']:
            sql_condition.append(
                ' AND ing.ing_cat_id in %(keyword)s'
            )
            sql_param['keyword'] = params['keyword']

        sql = sql.format('\n'.join(sql_condition))
        ing_list = SQL.sql_to_list(
            sql=sql, params=sql_param)

        return JsonResponse(result=True, data=ing_list)       

    def get_cat_list(self):
        '''カテゴリーリスト取得'''

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            cat.cat_name,
            cat.id,
            cat.cat_no,
            cat.parent_id
        FROM
            mst_ingredients_cat       cat
        ORDER BY
            cat.cat_no
        '''

        sql = '''
        SELECT
            cat.cat_name,
            cat.id,
            cat.hierarchy_path,
            cat.parent_id
        FROM
            mst_ingredients_cat       cat
        ORDER BY
            cat.hierarchy_path
        '''

        cat_list = SQL.sql_to_list(sql=sql)

        for cat in cat_list:
            cat['levels'] = list(range(cat['hierarchy_path'].count('/')))

        return cat_list 

    def get_category(self, request, params):
        ingredient = {}
        menu = {}
        for obj in MstIngredients.objects.all():
            index = obj.ing_cat_id
            if index not in ingredient:
                ingredient[index] = []
            ingredient[index].append(
                {'id': obj.id, 'name': obj.ing_name, 'unit': obj.consumption_unit, 'price':obj.ave_price}
            )
        
        sql = '''
                SELECT
                    mst.id,
                    mst.no,
                    mst.name,
                    cat.category_id as cat_id,
                    costs.price
                FROM
                    menu mst
                    LEFT JOIN menu_category cat ON cat.menu_id = mst.id
                    LEFT JOIN (
                        SELECT 
                            tbr.menu_id as menu_id,
                            sum(ing.ave_price * tbr.amount_to_use) as price
                        FROM
                            tbl_recipe tbr
                        LEFT JOIN
                            mst_ingredients ing
                        ON
                            tbr.ing_id = ing.id
                        GROUP BY
                            tbr.menu_id
                    ) as costs ON mst.id=costs.menu_id
            '''
        result = SQL.sql_to_list(sql)
        for item in result:
            index = item['cat_id']
            if index not in menu:
                menu[index] = []
            menu[index].append({
                'id': item['id'],
                'name': item['name'],
                'unit': '份',
                'price': item['price']
            })

        
        ingredient_cats = MstIngredientsCat.objects.all()
        category = []
        for item in ingredient_cats:
            if item.id in ingredient:
                category.append(
                    {
                        'id': item.id,
                        'name': item.cat_name,
                        'type': 1
                    }
            )
        sql = '''
            SELECT
                md.id,
                coalesce(md.display_name, md.name) AS name,
                2 as type
            FROM master_data md
            INNER JOIN master_data_group mdg ON md.group_id = mdg.id AND mdg.domain = 'menu_category'
        '''
        result = SQL.sql_to_list(sql)
        for item in result:
            if item['id'] in menu:
                category.append(item)

        
        data = {
            'category': category,
            'menu': menu,
            'ingredient': ingredient
        }
        return JsonResponse(result=True, data=data)
    
    def post_check(self, request, params):
        with transaction.atomic():
            try: 
                for row in params['lists']:
                    inspection = TblInspection()
                    inspection.part_id = row['data_id']
                    inspection.part_cat = row['cat_id']
                    inspection.part_type = row['cat_type']
                    inspection.part_unit = row['unit']
                    inspection.parts_unit_price = row['price']
                    inspection.parts_inventory_qty = row['stock']
                    inspection.inspection_date = params['inspection_date']
                    inspection.inspector = params['inspector']
                    inspection.remarks = params['remarks']
                    inspection.save()

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00023)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))