from master.models.role import *
from master.models.master import *
from master.models.menu import MenuCategory
from django.core.cache import cache
from django.conf import settings

import common.sql as Sql
from common.util import Util

from app.db.db_patch import SaasHandler


# TODO: 需要调查在清空缓存时，是否要加线程所，
# TODO: ★★★★★　为了避免不必要的冲突，对Master数据的操作，尽量放到闭店后

# return saas id
def cache_set(k, v):
    k = "{0}.{1}".format(SaasHandler.get_saas_id(), k)
    return cache.set(k, v)


def cache_get(k):
    k = "{0}.{1}".format(SaasHandler.get_saas_id(), k)
    return cache.get(k)

def clear_role():
    cache_set('role_user', None)
    cache_set('role_auth', None)


def clear_master():
    cache_set('master_data', None)
    cache_set('master_data_code', None)
    cache_set('master_by_menu', None)

# ＊＊＊＊＊＊＊＊＊＊＊＊＊＊ メニューを取得 ＊＊＊＊＊＊＊＊＊＊＊＊＊＊


def get_menu_list():
    return cache_get('get_menu_list')


def set_menu_list(cachedata):
    cache_set('get_menu_list', cachedata)


def get_menu_category(category_group):

    cachedata = cache_get('get_menu_category')
    if cachedata is None:
        cache_set('get_menu_category', {})
        cachedata = cache_get('get_menu_category')

    if category_group in cachedata:
        print("＊＊＊＊＊＊＊＊＊＊＊＊＊＊ メニューを取得 ＊＊＊＊＊＊＊＊＊＊＊＊＊＊")
        return cachedata[category_group]

    return None


def set_menu_category(category_group, data):
    cachedata = cache_get('get_menu_category')
    if cachedata is None:
        cache_set('get_menu_category', {})
        cachedata = cache_get('get_menu_category')

    cachedata[category_group] = data
    cache_set('get_menu_category', cachedata)
    # ＊＊＊＊＊＊＊＊＊＊＊＊＊＊ role user 関連 ＊＊＊＊＊＊＊＊＊＊＊＊＊＊


def create_role_cache():
    # cachedata = {(rec.user.id, rec.role) for rec in RoleUser.objects.all()}
    cachedata = {}
    for rec in RoleUser.objects.all():
        if rec.user.id in cachedata:
            role = cachedata[rec.user.id]

            # 権限レベル高いロールを利用
            # （※権限同じユーザ複数ロールに配属するのはできる限り下げたい）
            if rec.role.level > role.level:
                cachedata[rec.user.id] = rec.role
        else:
            cachedata[rec.user.id] = rec.role

    # ゲストロール設定
    cachedata["__geust__"] = Role.objects.get(name="guest")

    cache_set('role_user', cachedata)


def get_guest_role():
    cachedata = cache_get('role_user')
    if cachedata is None:
        create_role_cache()
        cachedata = cache_get('role_user')
    return cachedata["__geust__"]


def get_role(user):
    cachedata = cache_get('role_user')
    if cachedata is None:
        create_role_cache()
        cachedata = cache_get('role_user')

    if user.id in cachedata:
        return cachedata[user.id]

    return None

# ＊＊＊＊＊＊＊＊＊＊＊＊＊＊ role 制限関連 ＊＊＊＊＊＊＊＊＊＊＊＊＊＊
# cachedata = {
#   'role_id': {
#       'view1': [action1],
#       'view2': [action2, action3],
#       'view3': [action4],
#   }
# }
#


def create_role_detail_cache():
    cachedata = {}
    for rec in RoleDetail.objects.all():
        if rec.role.id not in cachedata:
            cachedata[rec.role.id] = {}

        if rec.view not in cachedata[rec.role.id]:
            cachedata[rec.role.id][rec.view] = [rec.action]
        else:
            cachedata[rec.role.id][rec.view].append(rec.action)

    cache_set('role_auth', cachedata)


def get_role_auth(role):
    cachedata = cache_get('role_auth')
    if cachedata is None:
        create_role_detail_cache()
        cachedata = cache_get('role_auth')

    return cachedata[role.id] if role.id in cachedata else None


# ＊＊＊＊＊＊＊＊＊＊＊＊＊＊ code　利用してマスタを取得 ＊＊＊＊＊＊＊＊＊＊＊＊＊＊

# def create_master_by_code_cache():
#     cachedata = {}
#     for master in MasterData.objects.all():

#         key = str(master.group.name) + str(master.code)

#         cachedata[key] = master

#     cache_set('master_data_code', cachedata)


def get_master_by_code(group_name, code):
    ''' code でマスタデータを取得'''

    key = str(group_name) + str(code)
    cachedata = cache_get('master_data_code')

    if cachedata is None:
        cachedata = {}

    if key in cachedata:
        return cachedata[key]

    master = MasterData.objects.get(code=code, group__name=group_name)
    cachedata[key] = master
    cache_set('master_data_code', cachedata)

    return master

# ＊＊＊＊＊＊＊＊＊＊＊＊＊＊ Kitchenの通信分類用　メニューと所属するマスタを紐づけ ＊＊＊＊＊＊＊＊＊＊＊＊＊＊
# 監視用分类，为每一种分类都要建立同学管道，浪费资源，所以只要决定一种即可(サーバクライアント側両方設定)


# def create_master_by_menu_cache():
#     cachedata = {}
#     for item in MenuCategory.objects.filter(category__group__name="menu_category_standard"):
#         cachedata[item.menu.id] = item.category.id

#     cache_set('master_by_menu', cachedata)


def get_master_by_menu(menu_id):
    ''' メニューと所属するマスタを取得'''
    cachedata = cache_get('master_by_menu')

    if cachedata is None:
        cachedata = {}

    if menu_id in cachedata:
        return cachedata[menu_id]

    menus = Sql.sql_to_dict('''
        SELECT menu.category_id,
            menu.menu_id
        FROM menu_category menu
        LEFT JOIN master_data master ON master.id = menu.category_id
        LEFT JOIN master_data_group master_group ON master_group.id = master.group_id
        WHERE master_group.name = 'menu_category_standard'
    ''')
    for item in menus:
        cachedata[item["menu_id"]] = item["category_id"]
    
    cache_set('master_by_menu', cachedata)
    return cachedata[menu_id]

