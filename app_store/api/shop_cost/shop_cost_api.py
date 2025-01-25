
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

import app.const as Const
import app.common.message as Message
import app.db.sql as SQL
import app.util as Util
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.exception.web import WebException
from app.db.models.store_table import ShopCost, ShopCostCat
from app.db.models.tbl import TblSupplie


class ShopCostApi(BaseAPI):

    def get_ing_data(self, request, params):
        '''費用データ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            cost.id,
            cost.cost_name,
            cost.cost_category_id,
            cost.pay_time,
            cost.cost
        FROM
            shop_cost       cost
        WHERE 1 = 1
            {0}
        ORDER BY
            cost.id
        '''

        if 'keyword' in params and params['keyword']:
            sql_condition.append(
                'AND (cost.cost_name LIKE %(keyword)s)'
            )
            sql_param['keyword'] = '%' + params['keyword'] + '%'

        if 'filter' in params and params['filter']:
            sql_condition.append(' AND cost.cost_category_id in %(filter)s')
            sql_param['filter'] = params['filter']

        sql = sql.format('\n'.join(sql_condition))
        cost_list = SQL.sql_to_list(sql=sql, params=sql_param, DB_name=DATA_BASE)

        cat_list = self.get_cat_list()
        
        parents = [c for c in cat_list if not c['parent_id']]
        for cat in parents:
            for child in cat_list:
                if child['parent_id'] == cat['id']:
                    child["category_name"] = cat["category_name"] + "/" + child["category_name"]

        for cost in cost_list:
            cost['category_name'] = ''.join([cat['category_name'] for cat in cat_list if cat['id'] == cost['cost_category_id']])

        parents = [c for c in cat_list if not c['parent_id']]
        for cat in parents:
            children = [c for c in cat_list if c['parent_id'] == cat['id']]
            cat['children'] = children

        data = {
            'rows': cost_list,
            'filter_cat': parents,
            'categories': cat_list
        }

        return JsonResponse(result=True, data=data)

    def get_edit_data(self, request, params):
        '''編集フォームのデータ取得'''

        result = []

        DATA_BASE = 'ami'

        if 'id' in params and params['id']:
            sql = '''
            SELECT
                cost.id,
                cost.cost_name,
                cost.cost_category_id,
                cost.pay_time,
                cost.cost
            FROM
                shop_cost       cost
            WHERE
                cost.id = %(id)s
            '''

            result = SQL.sql_to_list(sql=sql, params={'id': params['id']}, DB_name=DATA_BASE)
        
        cat_list = self.get_cat_list()
        
        parents = [c for c in cat_list if not c['parent_id']]
        categories = []
        for cat in parents:
            categories.append(cat)
            for child in cat_list:
                if child['parent_id'] == cat['id']:
                    child["category_name"] = "　" + child["category_name"]
                    categories.append(child)

        data = {
            'result': result[0] if result else {},
            'categories': categories,
        }

        return JsonResponse(result=True, data=data)

    def set_ing_data(self, request, params):
        '''費用データ保存'''

        DATA_BASE = 'ami'

        # 費用名重複チェック
        # exist = self.check_exist_cost_name(params)
        # if exist:
        #     return JsonResponse(result=False, message='入力された名前がすでに存在します')

        with transaction.atomic(using=DATA_BASE):
            try:
                if 'cost_id' in params and params['cost_id']:
                    ing = ShopCost.objects.using(DATA_BASE).get(pk=params['cost_id'])
                    ing.save(request=request, values=params, using=DATA_BASE)

                else:
                    ing = ShopCost()
                    ing.insert(request=request, values=params, using=DATA_BASE)

                cost_id = ing.pk
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005), data=cost_id)

    def check_exist_cost_name(self, params):
        '''重複チェック'''

        DATA_BASE = 'ami'
        sql_param = {}
        sql_condition = []

        sql = '''
        SELECT
            COUNT(0)
        FROM
            shop_cost cost
        WHERE
            cost.cost_name = %(cost_name)s
            {0}
        '''

        sql_param['cost_name'] = params['cost_name']

        if 'cost_id' in params and params['cost_id']:
            sql_condition.append(' AND cost.id != %(cost_id)s ')
            sql_param['cost_id'] = params['cost_id']

        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_one(sql=sql, params=sql_param, DB_name=DATA_BASE)

        if result > 0:
            return True
        else:
            return False

    def delete_ing_data(self, request, params):
        '''費用データ削除'''

        DATA_BASE = 'ami'
        with transaction.atomic(using=DATA_BASE):
            try:
                for row in params['rows']:
                    ing = ShopCost.objects.using(DATA_BASE).get(pk=row['id'])
                    ing.delete()
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def move_ing_data(self, request, params):
        '''費用カテゴリー移動'''

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                for row in params['rows']:
                    if 'id' in row and row['id']:
                        ing = ShopCost.objects.using(DATA_BASE).get(pk=row['id'])

                        # 選択されたカテゴリー保存
                        if 'cost_category_id' in params and params['cost_category_id']:
                            ing.cost_category_id = params['cost_category_id']
                            ing.save(using=DATA_BASE)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_cat_data(self, request, params):
        '''カテゴリーデータ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            cat.category_name,
            cat.id,
            cat.parent_id,
            cost.cost_total,
            cost.cost_count
        FROM
            shop_cost_category  cat
            left join ( select cost_category_id, count(1) as cost_count, sum(cost) as cost_total from shop_cost group by cost_category_id) cost on cat.id = cost.cost_category_id
        ORDER BY
            cat.id
        '''

        result = SQL.sql_to_list(sql=sql, params=sql_param, DB_name=DATA_BASE)

        parents = [c for c in result if not c['parent_id']]

        for cat in parents:
            children = [c for c in result if c['parent_id'] == cat['id']]
            cat['children'] = children
            cat['display'] = 'table-row'

        return JsonResponse(result=True, data=parents)

    def set_cat_data(self, request, params):
        '''カテゴリーデータ保存'''

        if not 'parent_id' in params:
            params['parent_id'] = None

        DATA_BASE = 'ami'

        exist = self.check_exist_category_name(params)

        if exist:
            return JsonResponse(result=False, message='入力された名前がすでに存在します')

        with transaction.atomic(using=DATA_BASE):
            try:
                if 'category_id' in params and params['category_id']:
                    cat = ShopCostCat.objects.using(DATA_BASE).get(pk=params['category_id'])

                else:
                    cat = ShopCostCat()
                    cat.insert(request=request, values=params, using=DATA_BASE)

                if params['parent_id']:
                    parent = ShopCostCat.objects.using(DATA_BASE).get(pk=params['parent_id'])
                #     params['hierarchy_path'] = str(parent.pk) + '/' + str(cat.pk)
                # else:
                #     params['hierarchy_path'] = str(cat.pk)

                cat.save(request=request, values=params, using=DATA_BASE)
                category_id = cat.pk

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005), data=category_id)

    def check_exist_category_name(self, params):
        '''重複チェック'''

        sql_condition = []
        sql_param = {}

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            COUNT(0)
        FROM
            shop_cost_category cat
        WHERE
            cat.category_name = %(category_name)s
            {0}
        '''

        if params['parent_id']:
            sql_condition.append(' AND cat.parent_id = %(parent_id)s ')
            sql_param['parent_id'] = params['parent_id']
        else:
            sql_condition.append(' AND cat.parent_id is NULL ')

        if 'category_id' in params and params['category_id']:
            sql_condition.append(' AND cat.id != %(category_id)s ')
            sql_param['category_id'] = params['category_id']

        sql_param['category_name'] = params['category_name']
        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_one(sql=sql, params=sql_param, DB_name=DATA_BASE)

        if result > 0:
            return True
        else:
            return False

    def delete_cat_data(self, request, params):
        '''カテゴリーデータ削除'''

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                for row in params['rows']:
                    if ShopCost.objects.using(DATA_BASE).filter(cost_category_id=row['id']).exists():
                        return JsonResponse(result=True, message='このカテゴリーの費用を削除してください。')

                    cat = ShopCostCat.objects.using(DATA_BASE).get(pk=row['id'])
                    cat.delete()

                    # ings = ShopCost.objects.using(DATA_BASE).filter(cost_category_id=row['id'])
                    # for ing in ings:
                    #     ing.cost_category_id = None
                    #     ing.save(request=request, using=DATA_BASE)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def move_cat_data(self, request, params):
        '''カテゴリー移動'''

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                for row in params['rows']:
                    cat = ShopCostCat.objects.using(DATA_BASE).get(pk=row['id'])
                    if 'parent_id' in params and params['parent_id']:
                        cat.parent_id = params['parent_id']
                        cat.hierarchy_path = str(params['parent_id']) + '/' + str(cat.pk)
                        cat.save(using=DATA_BASE)
                    else:
                        cat.parent_id = None
                        cat.hierarchy_path = str(cat.pk)
                        cat.save(using=DATA_BASE)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def get_cat_edit_data(self, request, params):
        '''カテゴリー編集データ取得'''

        DATA_BASE = 'ami'

        result = []

        if 'id' in params and params['id']:
            sql = '''
            SELECT
                cat.category_name,
                cat.id,
                cat.parent_id
            FROM
                shop_cost_category cat
            WHERE
                cat.id = %(id)s
            '''

            result = SQL.sql_to_list(sql=sql, params={'id': params['id']}, DB_name=DATA_BASE)

        sql = '''
        SELECT
            cat.category_name,
            cat.id
        FROM
            shop_cost_category cat
        WHERE
            cat.parent_id is NULL
        '''

        parents = SQL.sql_to_list(sql=sql, DB_name=DATA_BASE)

        data = {
            'result': result[0] if result else {},
            'parents': parents
        }

        return JsonResponse(result=True, data=data)

    def get_supplier(self, request, params):
        sql = "SELECT * FROM tbl_supplie"
        result = SQL.sql_to_list(sql=sql)
        return JsonResponse(result=True, data=result)
 
    
    def del_supplier(self, request, params):
        if 'id' in params and params['id']:
            TblSupplie.objects.filter(id=params['id']).delete()
        return JsonResponse(result=True)

    def set_supplier(self, request, params):
        supplier = TblSupplie()
        if 'id' in params and params['id']:
            supplier = TblSupplie.objects.get(pk=params['id'])
        else:
            if TblSupplie.objects.filter(sup_name=params['sup_name']).count()>0:
                return JsonResponse(result=False, message=params['sup_name'] + 'は存在します。')
        supplier.sup_name = params['sup_name']
        supplier.sup_tel = params['sup_tel']
        supplier.sup_addr = params['sup_addr']
        supplier.save()
        return JsonResponse(result=True)


    def get_cat_list(self):
        '''カテゴリーリスト取得'''

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            cat.category_name,
            cat.id,
            cat.parent_id
        FROM
            shop_cost_category cat
        ORDER BY
            cat.id
        '''

        cat_list = SQL.sql_to_list(sql=sql, params={}, DB_name=DATA_BASE)

        return cat_list
