import re
import json
from datetime import datetime, date
from django.forms.models import model_to_dict

import inspect
import app.db.sql as SQL
import os

from django.core.cache import cache
from redis.exceptions import ConnectionError
from app.log import logger
import traceback
import dateutil.parser


def support_datetime_default(o):
    if isinstance(o, date):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")


def encode(obj):
    json_str = json.dumps(obj, default=support_datetime_default)
    return json_str


def decode(json_str):
    obj = json.loads(json_str)
    return obj


def is_empty(obj):
    if obj == None:
        return True

    if isinstance(obj, str) and not obj:
        return True

    return True


def class_set_attrs(obj, attrs):
    ''' Dictの値を　クラスのインスタンスに自動セットする '''

    for key in obj.__dict__.keys():
        if key in attrs:
            setattr(obj, key, attrs[key])

    return True


def get_code(group_id=None):

    key = "get_code_" + group_id
    try:

        results = cache.get(key)

    except ConnectionError:
        results = None
        logger.error(" REDIS　接続エラー:\n" + traceback.format_exc())

    if not results:

        params = {}

        if group_id:
            params["group_id"] = group_id

        sql = SQL.get_sql("common.select_code")
        results = SQL.sql_to_list(sql, params)

        try:
            cache.set(key, results)
        except ConnectionError:
            logger.error(" REDIS　接続エラー:\n" + traceback.format_exc())

    return results


# def get_code(code_type=None, language='J'):
    
#     key = "get_code" + "_" + language + "_" + code_type
#     try:

#         results = cache.get(key)

#     except ConnectionError:
#         results = None
#         logger.error(" REDIS　接続エラー:\n" + traceback.format_exc())

#     if not results:

#         params = {}

#         if code_type:
#             params["code_type"] = code_type

#         if language:
#             params["language"] = language

#         sql = SQL.get_sql("common.select_code")
#         results = SQL.sql_to_list(sql, params)

#         try:
#             cache.set(key, results)
#         except ConnectionError:
#             logger.error(" REDIS　接続エラー:\n" + traceback.format_exc())

#     return results


# def get_code_multi(code_type_list, language='J'):

#     params = {}
#     if code_type_list:
#         params["code_type_list"] = tuple(code_type_list)

#     if language:
#         params["language"] = language

#     sql = SQL.get_sql("common.select_code_multi")
#     results = SQL.sql_to_list(sql, params)

#     return results


def get_files(path, file_filter="", matches=[]):
    ''' 指定フォルダしたのすべてファイルを取得し、 matchesにセット'''

    if file_filter:
        pattern = re.compile('.*\.(' + file_filter + ')$')

    for (dirpath, dirnames, filenames) in os.walk(path):

        for filename in filenames:

            if pattern.match(filename):
                matches.append(os.path.join(dirpath, filename))


def str_to_datetime(val):
    if val:
        day = dateutil.parser.parse(val)
    else:
        return val

    return day


# def str_to_datetime(val):
#     dt = dateutil.parser.parse(val)
#     return dt
