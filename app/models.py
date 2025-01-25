
from django.db import models as DjangoModel
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from app.db.models.base import BaseModel
import hashlib
import random
import string


class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, id, password, **extra_fields):
        # """メールアドレスでの登録を必須にする"""
        # if not email:
        #     raise ValueError('The given email must be set')
        # email = self.normalize_email(email)

        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, id, password=None, **extra_fields):
        # """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        return self._create_user(id, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""

        raise ValueError('既に利用しない')


class MstUser(BaseModel):

    USERNAME_FIELD = 'user_account'
    REQUIRED_FIELDS = []

    objects = UserManager()

    user_account = DjangoModel.CharField(max_length=30, blank=True, null=True)
    password = DjangoModel.CharField(max_length=500, blank=True, null=True)
    password_last_update_date = DjangoModel.DateField(blank=True, null=True)
    language = DjangoModel.CharField(max_length=50, blank=True, null=True)
    email = DjangoModel.CharField(max_length=100, blank=True, null=True)
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)


    # 固定にする（JWT設定用　カスタマイズするため固定にする）
    is_active = True

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.user_account

    def get_username(self):
        "Return the identifying username for this User"
        return self.user_account

    def create_password(self, password):
        """ユーザーマネージャー."""
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        md5_password = hl.hexdigest()

        return md5_password

    def create_onetime(self):
        """ユーザーマネージャー."""
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(10)]
        word = ''.join(randlst)
        print("==================== " + word + "====================")
        return word

    def check_password(self, password):
        """ユーザーマネージャー."""
        return self.password == self.create_password(password)

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        print("..........※※※※　....... is_anonymous(self):")
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        print("..........※※※※　....... is_authenticated(self):")
        return True

    last_login = None

    class Meta:
        managed = False
        db_table = 'mst_user'

        # print("has_permission")
        # try:
        #     getattr(request, "role")
        # except AttributeError:
        #     return False

        # # roles = get_role_auth(request.role)

        # # テストのため
        # return True

        # for viewname in roles:
        #     if viewname in str(view):
        #         if 'ALLOW' in roles.get(viewname):
        #             # すべて許可される場合
        #             return True
        #         elif request.method in roles.get(viewname):
        #             return True
        #         else:
        #             continue

        # return False
