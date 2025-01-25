import traceback
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils.module_loading import import_string
from setuptools import Command

from app.const import MessageIDs
from app.exception.web import WebException
from app.models import MstUser

import app.const as Const

from app.auth.user import AuthUser
import app.db.sql as SQL

from rest_framework import authentication
from app.http.response import JsonResponse
import app.common.message as Message
import web.settings as AppSettings

import datetime
import app.mail as Mail


class AuthBackend(authentication.BaseAuthentication):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, user_account=None, password=None):

        # for line in traceback.format_stack():
        #     print(line.strip())

        # login_valid = (settings.ADMIN_LOGIN == username)
        # pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        # if login_valid and pwd_valid:
        #     try:
        #         user = User.objects.get(username=username)
        #     except User.DoesNotExist:
        #         # Create a new user. There's no need to set a password
        #         # because only the password from settings.py is checked.
        #         user = User(username=username)
        #         user.is_staff = True
        #         user.is_superuser = True
        #         user.save()
        #     return user
        # return None

        if "," in user_account and user_account:
            p_user_account, p_language = str(user_account).split(",")
        else:
            raise WebException(message=Message.get_by_id(Const.MessageIDs.MQ00023, p_language))

        try:
            user = MstUser.objects.get(user_account=p_user_account)
        except ObjectDoesNotExist:
            raise WebException(message=Message.get_by_id(Const.MessageIDs.MQ00023, p_language))
        # user = MstUser()

        # 回数チェック
        # if user.account_lock_times and user.account_lock_times >= AppSettings.APP["MAX_ACCOUNT_LOCK_TIMES"]:

        #     raise WebException(message=Message.get_by_id(Const.MessageIDs.MQ00032, p_language))

        # # 有効チェック
        # if user.id_delete_date and user.id_delete_date <= datetime.datetime.now().date():
        #     raise WebException(message=Message.get_by_id(Const.MessageIDs.MQ00023, p_language))

        #　パスワードチェック
        if user.create_password(password) != user.password:
            if not user.account_lock_times:
                user.account_lock_times = 0
            user.account_lock_times += 1

            if user.account_lock_times == AppSettings.APP["MAX_ACCOUNT_LOCK_TIMES"]:
                # 回数上限に達する場合ワンタイムパスワード発行
                word = user.create_onetime()
                user.one_time_password_issue = "1"
                user.password = user.create_password(word)
                if user.email:
                    mail_body = '''
                        回数上限に達しました、セキュリティ回避のため、ワンタイムパスワードは下記に発行しました。
                        「{0}」
                    '''.format(word)
                    Mail.send("【APP2】ワンタイムパスワードお知らせ", mail_body, user.email)

            user.save()
            raise WebException(message=Message.get_by_id(Const.MessageIDs.MQ00023, p_language))


        sql = '''
        SELECT
            U.ID USER_ID,
            U.USER_ACCOUNT,
            U.USER_NAME
        FROM 
            MST_USER U
        WHERE 
            U.USER_ACCOUNT = %(USER_ACCOUNT)s
        '''
        data = SQL.sql_to_list(sql, {"USER_ACCOUNT": p_user_account})
        if len(data) == 0:
            raise WebException(Const.MessageIDs.MQ00023)

        auth_user = AuthUser(init_data=data[0])

        for key in AppSettings.AUTH_OPTION:
            self.load_class(AppSettings.AUTH_OPTION[key]).auth(auth_user)

        auth_user.authority = self.get_authority(auth_user)
        auth_user.authenticated = True
        auth_user.language = p_language
        
        return auth_user

    def get_user(self, user_account):
        try:
            return MstUser.objects.get(user_account=user_account)
        except MstUser.DoesNotExist:
            return None
    
    def get_authority(self, user):

        sql_param = {}
        sql_param["role_id"] = user.options["role_id"]
        sql_param["company_id"] = user.options["company_id"]
        sql_param["org_id"] = user.options["org_id"]

        sql = '''
        SELECT
            auth.id
        FROM
            mst_authority auth
        WHERE
            auth.role_id = %(role_id)s
            AND auth.company_id = %(company_id)s
            AND auth.organization_id = %(org_id)s
        '''
        data = SQL.sql_to_array(sql, sql_param)
        
        if len(data) == 0:
            return
        
        return data[0]
    
    def load_class(self, path):
        return import_string(path)()
