
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

import app.const as Const
import app.common.message as Message
import app.db.sql as SQL
import app.util as Util
from app.http.api import BaseAPI
from app.http.response import JsonResponse
from app.exception.web import WebException
from app.db.models.store_table import MstIngredients, MstIngredientsCat
from django.db.models import Max


class IngredientsApi(BaseAPI):

    def get_ing_data(self, request, params):
        '''材料データ取得'''

        sql_param = {}
        sql_condition = []

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            ing.id,
            ing.ing_no,
            ing.ing_name,
            ing.ing_cat_id,
            ing.ave_price || '円' || COALESCE('/' || ing.stock_unit, '') AS ave_price
        FROM
            mst_ingredients       ing
        WHERE 1 = 1
            {0}
        ORDER BY
            ing.ing_no
        '''

        if 'keyword' in params and params['keyword']:
            sql_condition.append(
                ' AND (ing.ing_no LIKE %(keyword)s'
                'OR ing.ing_name LIKE %(keyword)s)'
            )
            sql_param['keyword'] = '%' + params['keyword'] + '%'

        if 'filter' in params and params['filter']:
            sql_condition.append(' AND ing.ing_cat_id in %(filter)s')
            sql_param['filter'] = params['filter']

        sql = sql.format('\n'.join(sql_condition))
        ing_list = SQL.sql_to_list(
            sql=sql, params=sql_param, DB_name=DATA_BASE)

        sql = '''
        SELECT
            id,
            cat_name,
            hierarchy_path
        FROM
            mst_ingredients_cat
        '''

        cat_list = SQL.sql_to_list(sql=sql, DB_name=DATA_BASE)

        for cat in cat_list:
            paths = []
            cat_path = []
            if cat['hierarchy_path']:
                paths = cat['hierarchy_path'].split('/')
            for path in paths:
                name = [cat['cat_name']
                        for cat in cat_list if cat['id'] == int(path)]
                cat_path.append(name[0])
            cat['cat_name'] = '／'.join(cat_path)

        for ing in ing_list:
            ing['cat_name'] = ''.join(
                [cat['cat_name'] for cat in cat_list if cat['id'] == ing['ing_cat_id']])

        category = self.get_cat_list()
        parents = [c for c in category if not c['parent_id']]
        for cat in parents:
            children = [c for c in category if c['parent_id'] == cat['id']]
            cat['children'] = children

        data = {
            'rows': ing_list,
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
                ing.id,
                ing.ing_no,
                ing.ing_name,
                ing.ing_cat_id,
                ing.stock_unit,
                ing.consumption_unit,
                ing.unit_conv_rate,
                ing.ave_price
            FROM
                mst_ingredients       ing
            WHERE
                ing.id = %(id)s
            '''

            result = SQL.sql_to_list(
                sql=sql, params={'id': params['id']}, DB_name=DATA_BASE)

        data = {
            'result': result[0] if result else {},
            'categories': self.get_cat_list(),
        }

        return JsonResponse(result=True, data=data)

    def set_ing_data(self, request, params):
        '''材料データ保存'''

        DATA_BASE = 'ami'

        # 材料名重複チェック
        exist = self.check_exist_ing_name(params)
        if exist:
            return JsonResponse(result=False, message='入力された名前がすでに存在します')

        with transaction.atomic(using=DATA_BASE):
            try:
                if 'ing_id' in params and params['ing_id']:
                    ing = MstIngredients.objects.using(
                        DATA_BASE).get(pk=params['ing_id'])
                    ing.save(request=request, values=params, using=DATA_BASE)

                else:
                    ing = MstIngredients()
                    ing.insert(request=request, values=params, using=DATA_BASE)

                ing_id = ing.pk
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005), data=ing_id)

    def check_exist_ing_name(self, params):
        '''重複チェック'''

        DATA_BASE = 'ami'
        sql_param = {}
        sql_condition = []

        sql = '''
        SELECT
            COUNT(0)
        FROM
            mst_ingredients        ing
        WHERE
            ing.ing_name = %(ing_name)s
            {0}
        '''

        sql_param['ing_name'] = params['ing_name']

        if 'ing_id' in params and params['ing_id']:
            sql_condition.append(' AND ing.id != %(ing_id)s ')
            sql_param['ing_id'] = params['ing_id']

        sql = sql.format('\n'.join(sql_condition))
        result = SQL.sql_to_one(sql=sql, params=sql_param, DB_name=DATA_BASE)

        if result > 0:
            return True
        else:
            return False

    def delete_ing_data(self, request, params):
        '''材料データ削除'''

        DATA_BASE = 'ami'
        with transaction.atomic(using=DATA_BASE):
            try:
                for row in params['rows']:
                    ing = MstIngredients.objects.using(
                        DATA_BASE).get(pk=row['id'])
                    ing.delete()
            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def move_ing_data(self, request, params):
        '''材料カテゴリー移動'''

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                for row in params['rows']:
                    if 'id' in row and row['id']:
                        ing = MstIngredients.objects.using(
                            DATA_BASE).get(pk=row['id'])

                        # 選択されたカテゴリー保存
                        if 'ing_cat_id' in params and params['ing_cat_id']:
                            ing.ing_cat_id = params['ing_cat_id']
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
            cat.cat_name,
            cat.id,
            cat.cat_no,
            cat.explanation,
            cat.hierarchy_path,
            cat.parent_id
        FROM
            mst_ingredients_cat       cat
        ORDER BY
            cat.cat_no
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

        exist = self.check_exist_cat_name(params)

        if exist:
            return JsonResponse(result=False, message='入力された名前がすでに存在します')

        with transaction.atomic(using=DATA_BASE):
            try:
                if 'cat_id' in params and params['cat_id']:
                    cat = MstIngredientsCat.objects.using(
                        DATA_BASE).get(pk=params['cat_id'])

                else:
                    cat = MstIngredientsCat()
                    cat.insert(request=request, values=params, using=DATA_BASE)
                    cat.cat_no = self.getCatNo()

                if params['parent_id']:
                    parent = MstIngredientsCat.objects.using(
                        DATA_BASE).get(pk=params['parent_id'])
                    params['hierarchy_path'] = str(
                        parent.pk) + '/' + str(cat.pk)
                else:
                    params['hierarchy_path'] = str(cat.pk)

                cat.save(request=request, values=params, using=DATA_BASE)
                cat_id = cat.pk

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005), data=cat_id)

    def getCatNo(self):
        cat_no = MstIngredientsCat.objects.aggregate(Max('cat_no'))['cat_no__max'] or 0
        return cat_no + 1

    def check_exist_cat_name(self, params):
        '''重複チェック'''

        sql_condition = []
        sql_param = {}

        DATA_BASE = 'ami'

        sql = '''
        SELECT
            COUNT(0)
        FROM
            mst_ingredients_cat       cat
        WHERE
            cat.cat_name = %(cat_name)s
            {0}
        '''

        if params['parent_id']:
            sql_condition.append(' AND cat.parent_id = %(parent_id)s ')
            sql_param['parent_id'] = params['parent_id']
        else:
            sql_condition.append(' AND cat.parent_id is NULL ')

        if 'cat_id' in params and params['cat_id']:
            sql_condition.append(' AND cat.id != %(cat_id)s ')
            sql_param['cat_id'] = params['cat_id']

        sql_param['cat_name'] = params['cat_name']
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
                    cat = MstIngredientsCat.objects.using(
                        DATA_BASE).get(pk=row['id'])
                    cat.delete()

                    ings = MstIngredients.objects.using(
                        DATA_BASE).filter(ing_cat_id=row['id'])
                    for ing in ings:
                        ing.ing_cat_id = None
                        ing.save(request=request, using=DATA_BASE)

            except ObjectDoesNotExist:
                raise WebException(Const.MessageIDs.MQ00030)

        return JsonResponse(result=True, message=Message.get_by_id(Const.MessageIDs.MQ00005))

    def move_cat_data(self, request, params):
        '''カテゴリー移動'''

        DATA_BASE = 'ami'

        with transaction.atomic(using=DATA_BASE):
            try:
                for row in params['rows']:
                    cat = MstIngredientsCat.objects.using(
                        DATA_BASE).get(pk=row['id'])
                    if 'parent_id' in params and params['parent_id']:
                        cat.parent_id = params['parent_id']
                        cat.hierarchy_path = str(
                            params['parent_id']) + '/' + str(cat.pk)
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
                cat.cat_name,
                cat.id,
                cat.cat_no,
                cat.explanation,
                cat.parent_id
            FROM
                mst_ingredients_cat       cat
            WHERE
                cat.id = %(id)s
            '''

            result = SQL.sql_to_list(
                sql=sql, params={'id': params['id']}, DB_name=DATA_BASE)

        sql = '''
        SELECT
            cat.cat_name,
            cat.id
        FROM
            mst_ingredients_cat       cat
        WHERE
            cat.parent_id is NULL
        '''

        parents = SQL.sql_to_list(sql=sql, DB_name=DATA_BASE)

        data = {
            'result': result[0] if result else {},
            'parents': parents
        }

        return JsonResponse(result=True, data=data)

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

        cat_list = SQL.sql_to_list(sql=sql, params={}, DB_name=DATA_BASE)

        for cat in cat_list:
            cat['levels'] = list(range(cat['hierarchy_path'].count('/')))

        return cat_list
