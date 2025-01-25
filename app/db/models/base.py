from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import connection
import datetime
import app.db.sql as SQL
from app.exception.web import WebException
import app.const as Const
import app.util as Util
import time
import app.util as Util


class BaseModel(models.Model):

    def next_value(self):
        cursor = connection.cursor()
        cursor.execute("SELECT nextval(\'" + self._meta.db_table +
                       "_id_seq\');")
        result = cursor.fetchone()
        return result[0]

    """
    """
    # id = models.IntegerField(primary_key=True)

    # create_datetime = models.DateTimeField(verbose_name=_('作成日'), null=True, default=timezone.now,)
    # create_user = models.CharField(verbose_name=_('作成者'), blank=True, null=True, max_length=64,)
    # create_programe = models.CharField(verbose_name=_('作成プログラム'), blank=True, null=True, max_length=64,)
    # update_datetime = models.DateTimeField(verbose_name=_('最終更新日'), null=True, default=timezone.now,)
    # update_user = models.CharField(verbose_name=_('最終更新者'), blank=True, null=True, max_length=64,)
    # update_programe = models.CharField(verbose_name=_('最終更新プログラム'), blank=True, null=True, max_length=64,)
    # def clean(self):
    #     # Don't allow draft entries to have a pub_date.
    #     if hasattr(self, "last_update_date"):
    #         raise ValidationError({'pub_date': _('Draft entries may not have a publication date.')})

    def insert(self, values=None, request=None, *args, **kwargs):
        # if Video.objects.filter(field_boolean=True).exists():
        #     print('Video with field_boolean=True exists')
        # else:

        self.setValues(values)

        if hasattr(self, "create_date"):
            self.create_date = datetime.datetime.now()

        if request and hasattr(self, "create_user_id") and hasattr(request.user, "user_id"):
            self.create_user_id = request.user.user_id

        if hasattr(self, "create_program") and request:
            self.create_program = request.path

        if hasattr(self, "last_update_date"):
            self.last_update_date = datetime.datetime.now()

        if request and hasattr(self, "last_update_user_id") and hasattr(request.user, "user_id"):
            self.last_update_user_id = request.user.user_id

        if hasattr(self, "last_update_program") and request:
            self.last_update_program = request.path

        # if hasattr(self, "id") and not self.id:
        #     self.id = self.next_value()

        super(BaseModel, self).save(*args, **kwargs)

    def save(self, values=None, request=None, *args, **kwargs):
        # if Video.objects.filter(field_boolean=True).exists():
        #     print('Video with field_boolean=True exists')
        # else:

        self.setValues(values)

        if hasattr(self, "last_update_date"):
            self.last_update_date = datetime.datetime.now()

        if request and hasattr(self, "last_update_user_id") and hasattr(request.user, "user_id"):
            self.last_update_user_id = request.user.user_id

        if hasattr(self, "last_update_program") and request:
            self.last_update_program = request.path

        super(BaseModel, self).save(*args, **kwargs)

    def update(self, values=None, request=None, using='default', *args, **kwargs):
        ''' 排他処理含む更新 '''
        # if Video.objects.filter(field_boolean=True).exists():
        #     print('Video with field_boolean=True exists')
        # else:

        self.setValues(values)

        if not hasattr(self, "last_update_date"):
            raise("開発段階エラー：排他処理は「last_update_date」が必要となります。")

        last_update_date = self.last_update_date

        if request and hasattr(self, "last_update_user_id") and hasattr(request.user, "user_id"):
            self.last_update_user_id = request.user.user_id

        if hasattr(self, "last_update_program") and request:
            self.last_update_program = request.path

        # current = datetime.datetime.now()
        if (not hasattr(self, '_meta')) or (not 'db_table' in self._meta.__dict__):
            raise("開発段階エラー：排他処理は「db_table」が必要となります。")

        table_name = self._meta.db_table

        if (not hasattr(self, 'id')) or (not self.id):
            raise("開発段階エラー：排他処理は「id」が必要となります。")

        update_sql_set = 'last_update_date=%(current_date)s,'
        # if type(last_update_date) == 'str':
        #     last_update_date = datetime.datetime.strptime(last_update_date, '%y-%m-%d %H:%M:%S.%f')

        update_params = {
            'id': self.id,
            'last_update_date': last_update_date,
            'current_date': datetime.datetime.now()
        }
        for obj_k, obj_v in self.__dict__.items():
            obj_k = obj_k.lower()
            if obj_k and obj_k[0:1] == '_':
                continue
            if obj_k == 'id' or obj_k == 'last_update_date':
                continue

            update_params[obj_k] = obj_v
            update_sql_set = update_sql_set + obj_k + '=%(' + obj_k + ')s,'

        update_sql = 'UPDATE ' + table_name + ' SET ' + update_sql_set.rstrip(',') + ' WHERE id=%(id)s AND last_update_date=%(last_update_date)s'
        SQL.execute(sql=update_sql, params=update_params, DB_name=using)

        # select date check
        r = SQL.sql_to_list("SELECT id FROM " + table_name + " WHERE id=%(id)s AND last_update_date=%(current_date)s",
                            params={'id': update_params['id'], 'current_date': update_params['current_date']}, DB_name=using)
        # update error
        if len(r) < 1:
            raise WebException('該当データは他のユーザより更新しましたのため、更新できませんご確認してください！')

        return

        # return current == self.last_update_date

    def setValues(self, values):

        datetime_list = []

        for field in self._meta.fields:
            if isinstance(field, models.DateField) or isinstance(field, models.DateTimeField):
                datetime_list.append(field.attname)

        if values:
            for key in values:
                col_name = key.lower()
                if hasattr(self, col_name):
                    if values[key] or isinstance(values[key], bool) or isinstance(values[key], int):
                        value = values[key]
                    else:
                        value = None

                    if col_name in datetime_list and isinstance(value, str):
                        value = Util.str_to_datetime(value)

                    setattr(self, col_name, value)

    class Meta:
        abstract = True
