

from os.path import dirname, abspath
from os import walk
from django.core.cache import cache
from django.apps import apps
from django.db import connection, connections
from django.conf import settings
from app.log import logger
import sys
import os
import re

from redis.exceptions import ConnectionError
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


def execute(sql="", params=[], sql_id="", DB_name='default'):
    '''
        更新系SQL

        # # 事务处理開始
        # with transaction.atomic():
        #     result = Sql.execute("insert into seat_status_history select * from seat_status ");
        #     print("########## Insert Select Test ##############")
        #     print(result)
    '''
    if not sql and sql_id:
        exe_sql = get_sql(sql_id)
    else:
        exe_sql = sql

    # logger.info("\n" + exe_sql+"\n")
    # logger.info(params)

    con = connections[DB_name]
    with con.cursor() as cursor:
        cursor.execute(sql, params)
        # result = cursor.fetchall()
    return None

def alert_date_formt(format):

    with connection.cursor() as cursor:
        cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT='{0}'".format(format))
        # result = cursor.fetchall()
    return None

def sql_to_list(sql="", params=[], sql_id="", DB_name='default'):
    '''　辞書型リスト　取る'''

    exe_sql, exe_params = __creat_sql_and_params(sql=sql, params=params, sql_id=sql_id)
    # cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    con = connections[DB_name]
    with con.cursor() as cursor:
        # cursor.execute("ALTER SESSION SET NLS_TERRITORY = 'JAPAN' ")
        cursor.execute(exe_sql, exe_params)
        rows = dictfetchall(cursor)
    return rows


# def anotherDB_sql_to_list(sql="", params=[], sql_id="", DB_name=''):
#     '''　DB「ami」で実行'''

#     exe_sql, exe_params = __creat_sql_and_params(sql=sql, params=params, sql_id=sql_id)
#     # cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     con = connections[DB_name]
#     with con.cursor() as cursor:
#         # cursor.execute("ALTER SESSION SET NLS_TERRITORY = 'JAPAN' ")
#         cursor.execute(exe_sql, exe_params)
#         rows = dictfetchall(cursor)
#     return rows

def sql_to_array(sql="", params=[], sql_id="", DB_name='default'):
    '''　辞書型1件の配列　取る　'''

    exe_sql, exe_params = __creat_sql_and_params(sql=sql, params=params, sql_id=sql_id)

    con = connections[DB_name]
    with con.cursor() as cursor:
        cursor.execute(exe_sql, exe_params)
        array = [row[0] for row in cursor.fetchall()]
    return array


def sql_to_one(sql="", params=[], sql_id="", DB_name='default'):
    '''　辞書型1個　取る　'''

    exe_sql, exe_params = __creat_sql_and_params(sql=sql, params=params, sql_id=sql_id)

    con = connections[DB_name]
    with con.cursor() as cursor:
        cursor.execute(exe_sql, exe_params)
        data = cursor.fetchone()
        if isinstance(data, tuple):
            result, = data
        else:
            result = None
    return result


def __creat_sql_and_params(sql="", params=[], sql_id=""):
    '''　辞書型リスト　取る'''

    if not sql and sql_id:
        exe_sql = get_sql(sql_id)
    else:
        exe_sql = sql

    result = re.findall("(?i)IN[ ]+\%\(([a-zA-Z0-9_]+)\)s", exe_sql)
    params_in = list(set(result))

    result = re.findall("\%\(([a-zA-Z0-9_]+)\)s", exe_sql)
    exe_params = {}
    for key in list(set(result)):
        if key in params_in:
            # IN SQL分存在する場合
            #　TODO：共通SQLセキュリティーチェックが必要
            sql_in = " (" + str(params[key])[1:-1]+") "
            exe_sql = exe_sql.replace("%("+key+")s", sql_in)
            continue

        exe_params[key] = params[key]

    # #時間型変更
    # exe_sql = re.sub(r"\'DS\'", "", exe_sql)

    # logger.info("\n" + exe_sql + "\n")
    # logger.info(exe_params)

    return (exe_sql, exe_params)


def init_sql_cache():

    try:

        path = settings.SQL_TEMPLATE_PATH
        abs_path = abspath(path)
        # print("[... path .....] " + path)
        if not os.path.exists(path):
            logger.error("パス「{0}」は存在しない".format(path))
            return

        for (dirpath, dirnames, filenames) in walk(path):

            # print("[... filename ..... {0},{1},{2}] ".format(dirpath, dirnames, filenames))

            for filename in filenames:

                if not filename.endswith(".sql"):
                    continue

                filepath = os.path.join(dirpath, filename)

                with open(filepath, 'r',  encoding='utf-8') as file:
                    lines = file.readlines()
                    newlines = []
                    for line in lines:

                        if line.find("　", 0) > 0:
                            logger.error("ファイル「{0}」に全角スペース含まれている".format(filename))
                        newlines.append(re.sub(r'\-\-[\s\S].*$', ' ', line))

                    abs_dirpath = abspath(dirpath).replace(abs_path, "")
                    abs_dirpath = re.sub('^(\\\\|\\|\/\/|\/)', "", abs_dirpath)
                    key = re.sub('\\\\|\\|\/\/|\/', ".", abs_dirpath) + "." + filename.replace('.sql', '')
                    # key = dirpath.replace(path+"\\", "").replace(path+"\/", "").replace('\\', '.').replace('\/', '.') + "." + filename.replace('.sql', '')
                    value = "".join(newlines)  # file.read()  # .replace('\n', ' ')
                    # print("[... filename .....]" + key)
                    SqlStore.set_sql(key, value)

    except Exception:
        logger.error("Unexpected error: {0} \n ※SQLファイル問題があるか、ご確かめてください！".format(sys.exc_info()[0]))


def get_sql(sql_name):
    ''' SQL文取得。 '''

    sql = SqlStore.get(sql_name)
    if not sql:
        init_sql_cache()
        sql = SqlStore.get(sql_name)

    if isinstance(sql, dict):
        return sql["sql"]

    return sql


def sql_to_page(sql_name="", sql_param={}, sql_condition=[], request_param={}, sql=None):
    ''' SQL文取得。

    Args:
        sql_name(string):　sql名
        sql_param(dict):　sql組み立て用パラメータ
        sql_condition(dict):　sql名実行パラメータ　※SQLインジェクション防止対策
        params(dict):　Language, rownumのFROM,TOなどの共通パラメータ取得するため
    '''
    if sql:
        sql_key = hash(sql)
        SqlStore.set_sql(sql_key, __analysis_sql(sql))
        sql_obj = SqlStore.get(sql_key)
    else:
        sql_obj = SqlStore.get(sql_name)

        if not sql_obj:
            init_sql_cache()
            sql_obj = SqlStore.get(sql_name)

        # SQLは文字列の場合、分析する。
        if isinstance(sql_obj, str):
            SqlStore.set_sql(sql_name, __analysis_sql(sql_obj))
            sql_obj = SqlStore.get(sql_name)

    # count取得
    sql_count = sql_obj["count"]
    sql_count = sql_count.format(*sql_condition)
    result = re.findall("\%\(([a-zA-Z0-9_]+)\)s", sql_count)
    exe_params = {}
    for key in list(set(result)):
        exe_params[key] = (sql_param[key] if key in sql_param else request_param[key])
    count = sql_to_one(sql_count, exe_params)

    sql_page = sql_obj["page"]
    sql_page = sql_page.format(*sql_condition)
    result = re.findall("\%\(([a-zA-Z0-9_]+)\)s", sql_page)
    exe_params = {}
    for key in list(set(result)):
        exe_params[key] = (sql_param[key] if key in sql_param else request_param[key])

    # ページ数とサイズ合わない場合調整
    page_size = int(exe_params["ROWNUM_TO"]) - int(exe_params["ROWNUM_FROM"]) + 1
    if count < page_size:
        exe_params["ROWNUM_FROM"] = 1
        exe_params["ROWNUM_TO"] = count

    if int(exe_params["ROWNUM_FROM"]) > count:
        exe_params["ROWNUM_FROM"] = 1
        exe_params["ROWNUM_TO"] = page_size

    rows = sql_to_list(sql_page, exe_params)

    return {
        "count": count,
        "rows": rows
    }


def __analysis_sql(sql):
    ''' SQLを解析する、一般画面向けではない '''

    analysis_sql = sql.upper()

    # ORDER BY 分析
    new_order_by = ""
    order_by = ""
    index_order = analysis_sql.rfind("ORDER BY ")
    if index_order < 0:
        raise("開発エラー：改ページSQL解析失敗, 「ORDER BY」が必須です。: {0}".format(sql))

    order_by = sql[index_order:]
    new_order_by = re.sub(r'[ ]+[a-zA-Z0-9_]+\.', " TBL.", order_by)
    new_order_by = re.sub(r'[,]+[a-zA-Z0-9_]+\.', " ,TBL.", new_order_by)

    # SELECT 分析
    index_select = analysis_sql.find("SELECT")
    rno = '''
    SELECT
    ROW_NUMBER() OVER(
        {0}
    ) AS RNO,
    '''.format(order_by)

    old_sql = rno + sql[(index_select + 6):]

    new_sql = '''
    SELECT
    *
    FROM (
    {0}
    ) TBL
    WHERE RNO BETWEEN %(ROWNUM_FROM)s AND %(ROWNUM_TO)s
    {1}
    '''.format(old_sql, new_order_by)

    # # FROM 分析 (FROM前後可能性おおいため、正規表現で検索する)
    # match = re.search(r'[ |\n]+FROM[ |\n]+', analysis_sql)
    # if match == None:
    #     raise("開発エラー：改ページSQL解析失敗, 「FROM」確認してください。: {0}".format(sql))

    # index_from = analysis_sql.find(match.group(0))
    # new_from = sql[index_from:]
    # new_sql_count = "SELECT COUNT(0) " + new_from

    # COUNT分解析

    # order byを消す
    sql = sql.replace(order_by, "")
    count_sql = re.sub("(?i)\(SELECT", "( \nSELECT", sql)
    count_sql = re.sub("(?i)SELECT\(", " SELECT \n(", count_sql)
    count_sql = re.sub("(?i)FROM\(", "FROM \n (", count_sql)
    count_sql = re.sub('[ |\n]+(?i)FROM[ |\n]+', " FROM ", count_sql)
    count_sql = re.sub('(^(?i)SELECT)|([ |\n]+(?i)SELECT[ |\n]+)', " SELECT ", count_sql)
    matchs = re.split('(^(?i)SELECT)|([ |\n]+FROM[ |\n]+)|([ |\n]+SELECT[ |\n]+)', count_sql)

    cnt = 0
    is_start = False
    index = 0
    lst = [item for item in matchs if item]
    for m in lst:

        if m and m.find(" SELECT ") >= 0:
            is_start = True
            cnt += 1

        if m and m.find(" FROM ") >= 0:
            cnt -= 1

        if is_start and cnt == 0:
            index += 1
            break

        index += 1
    new_sql_count = " SELECT COUNT(0) FROM " + " ".join(lst[index:])

    return {
        "sql": sql,
        "count": new_sql_count,
        "page": new_sql
    }


# def create_rownum_params(params):
#     ''' SQL文取得。 '''
#     page = int(params["__page"])
#     size = int(params["__size"])
#     return {
#         # "ROWNUM_FROM": (page - 1) * size + 1,
#         # "ROWNUM_TO": page * size
#         "from": (page - 1) * size + 1,
#         "to": page * size
#     }

# SQLキャッシュ関連


class SqlStore(object):
    __store = {}

    @classmethod
    def set_sql(cls, key, sql):
        ''' キャッシュにSQL追加 '''

        cls.__store[key] = sql

    # @classmethod
    # def set(cls, store):
    #     return cls.__store = store

    @classmethod
    def exist(cls, sql_name):
        return sql_name in cls.__store

    @classmethod
    def get(cls, sql_name, key=None):
        ''' キャッシュからSQLを取得 '''

        if cls.__store is None or len(cls.__store) == 0:
            return None

        if sql_name not in cls.__store:
            return None

        if isinstance(cls.__store[sql_name], str):
            return cls.__store[sql_name]

        if isinstance(cls.__store[sql_name], dict):
            if key:
                return cls.__store[sql_name][key]

            return cls.__store[sql_name]

        return None


# def get(id, appname=None):

#     sql_data = cache.get("sql_data")
#     try:
#         if sql_data is None:
#             create_sql_cache()
#             sql_data = cache.get("sql_data")
#     except ConnectionError:

#     except:
#         logger.error("Unexpected error: {0} \n ※SQLファイル問題があるか、ご確かめてください！".format(sys.exc_info()[0]))

#     sql = ""

#     if appname is None:
#         for key in sql_data:
#             if id in sql_data[key]:
#                 sql = sql_data[key][id]
#                 break
#     else:
#         sql = sql_data[appname][id]
#     # print(sql)
#     return sql
