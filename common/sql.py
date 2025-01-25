

from django.core.cache import cache
from django.apps import apps
from django.db import connection
from common.log import logger
import sys
import os
import re

#    cachedata = cache.get('role_user')


def dictfetchall(cursor):
    '''
        fetchallは一度に全部の結果をPythonの世界に持ってくるので、
        その呼び出しが終わったあとにはその百万行分のデータが全部Pythonのメモリ上に保持されます。

        fetchmanyは指定した分だけ結果を取って後はデータベースに留めておくので
        Pythonのメモリ上にはデータが少ししか保持されません。

        性能問題が出る場合、fetchmanyで改善すべき
    '''

    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def execute(sql, params=[]):
    '''
        更新系SQL

        # # 事务处理開始
        # with transaction.atomic():
        #     result = Sql.execute("insert into seat_status_history select * from seat_status ");
        #     print("########## Insert Select Test ##############")
        #     print(result)
    '''
    logger.info(sql)
    logger.info(params)

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        # result = cursor.fetchall()
    return None


def sql_to_dict(sql, params=[]):
    # logger.info(sql)
    # logger.info(params)
    # cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = dictfetchall(cursor)
    return rows


def sql_to_list(sql, params=[]):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        array = [row[0] for row in cursor.fetchall()]
    return array


def sql_to_one(sql, params=[]):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        result, = cursor.fetchone()
    return result


# SQLキャッシュ関連
def create_sql_cache():

    sql_data = {}
    for appname in apps.app_configs:
        cfg = apps.app_configs[appname]
        path = os.path.join(cfg.path, "sql")

        if not os.path.exists(path):
            continue

        for filename in os.listdir(path):
            if not filename.endswith(".sql"):
                continue

            if not (appname in sql_data):
                sql_data[appname] = {}

            filepath = os.path.join(path, filename)
            print(filename)
            with open(filepath, 'r',  encoding='utf-8') as file:
                lines = file.readlines()
                newlines = []
                for line in lines:
                    newlines.append(re.sub(r'\-\-[\s\S].*$', ' ', line))

                sqlStr = "".join(newlines)
                if sqlStr.find("　", 0) > 0:
                    print("！！！！！ファイル「{0}」に全角スペース含まれている".format(filename))
                sql_data[appname][filename.replace('.sql', '')] = "".join(newlines)  # file.read()  # .replace('\n', ' ')

    cache.set("sql_data", sql_data)


def get(id, appname=None):

    sql_data = cache.get("sql_data")
    try:
        if sql_data is None:
            create_sql_cache()
            sql_data = cache.get("sql_data")
    except:
        logger.error("Unexpected error: {0}".format(sys.exc_info()[0]))
        print("sql ファイル問題がある、ご確かめてください！")

    sql = ""

    if appname is None:
        for key in sql_data:
            if id in sql_data[key]:
                sql = sql_data[key][id]
                break
    else:
        sql = sql_data[appname][id]
    # print(sql)
    return sql
