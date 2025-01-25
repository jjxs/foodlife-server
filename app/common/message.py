import traceback
import app.db.sql as SQL
from django.core.cache import cache
from redis.exceptions import ConnectionError
from app.log import logger


def init_cache():
    messages = SQL.sql_to_list('''SELECT ID, LANGUAGE, MESSAGE FROM MST_MESSAGE ''')

    for msg in messages:
        key = msg["ID"] + "_" + msg["LANGUAGE"]
        cache.set(key, msg["MESSAGE"])


def get_by_id(id, language="J", params=None):
    '''J, E, CN'''
    key = id + "_" + language

    try:

        message = cache.get(key)

        if message:
            return message
    except ConnectionError:
        logger.error(" REDIS　接続エラー:\n" + traceback.format_exc())

    message = SQL.sql_to_one(
        '''SELECT MESSAGE FROM MST_MESSAGE WHERE ID = %(id)s AND LANGUAGE = %(language)s ''',
        params={"id": id, "language": language})

    return message


def get_all(language="J"):

    key = "ALL_MESSAGE_" + language

    try:

        messages = cache.get(key)

        if messages:
            return messages
    except ConnectionError:
        logger.error(" REDIS　接続エラー:\n" + traceback.format_exc())

    messages = SQL.sql_to_list(
        '''SELECT ID, MESSAGE FROM MST_MESSAGE WHERE LANGUAGE = %(language)s ''',
        params={"language": language})

    try:

        cache.set(key, messages)
    except ConnectionError:
        logger.error(" REDIS　接続エラー:\n" + traceback.format_exc())

    return messages
