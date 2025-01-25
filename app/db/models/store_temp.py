app starting...
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthMenu(models.Model):
    menu_path = models.CharField(unique=True, max_length=80)
    group_id = models.IntegerField(blank=True)

    class Meta:
        managed = False
        db_table = 'auth_menu'


class Machine(models.Model):
    sign = models.CharField(unique=True, max_length=128)
    update_data = models.DateTimeField()
    status = models.BooleanField()
    last_data = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'machine'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Counter(models.Model):
    is_pay = models.BooleanField(blank=True, null=True)
    is_split = models.BooleanField(blank=True, null=True)
    is_average = models.BooleanField(blank=True, null=True)
    is_input = models.BooleanField(blank=True, null=True)
    number = models.IntegerField()
    create_time = models.DateTimeField()
    delete = models.BooleanField(blank=True, null=True)
    delete_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    is_completed = models.BooleanField(blank=True, null=True)
    pay_price = models.IntegerField()
    tax_price = models.IntegerField()
    total_price = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'counter'


class CounterDetail(models.Model):
    no = models.CharField(max_length=64, blank=True, null=True)
    tax = models.DecimalField(
        max_digits=3, decimal_places=0, blank=True, null=True)
    total = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    pay = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    change = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    cut = models.DecimalField(
        max_digits=3, decimal_places=0, blank=True, null=True)
    reduce = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    canceled = models.BooleanField(blank=True, null=True)
    create_time = models.DateTimeField()
    canceled_type_id = models.IntegerField(blank=True, null=True)
    counter_id = models.IntegerField(blank=True, null=True)
    pay_method_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    amounts_actually = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    amounts_actually_tax = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    amounts_payable = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    cut_value = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    price_tax_in = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    tax_value = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'counter_detail'


class CounterDetailOrder(models.Model):
    order_detail_id = models.IntegerField()
    pay_count = models.IntegerField()
    is_delete = models.BooleanField(blank=True, null=True)
    is_ready = models.BooleanField(blank=True, null=True)
    is_split = models.BooleanField(blank=True, null=True)
    counter_id = models.IntegerField(blank=True, null=True)
    counter_detail_id = models.IntegerField(blank=True, null=True)
    pay_price = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    tax_in = models.BooleanField()
    ori_price = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'counter_detail_order'


class CounterSeat(models.Model):
    seat_id = models.IntegerField()
    seat_status_id = models.IntegerField()
    counter_no = models.CharField(max_length=64)
    counter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'counter_seat'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Guest(models.Model):
    no = models.IntegerField(blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    sur_name = models.CharField(max_length=100, blank=True, null=True)
    given_name = models.CharField(max_length=100, blank=True, null=True)
    sur_name_fricana = models.CharField(max_length=100, blank=True, null=True)
    given_name_fricana = models.CharField(
        max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    married = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField()
    is_temporary = models.BooleanField(blank=True, null=True)
    final_education_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest'


class GuestDevice(models.Model):
    device_id = models.CharField(max_length=512)
    device_name = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=1024, blank=True, null=True)
    created = models.DateTimeField()
    device_type_id = models.IntegerField(blank=True, null=True)
    guest_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'guest_device'


class GuestGroup(models.Model):
    name = models.CharField(max_length=200)
    evel_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest_group'


class GuestGroupDetail(models.Model):
    guest_id = models.IntegerField()
    guestgroup_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'guest_group_detail'


class GuestUser(models.Model):
    display_name = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField()
    settings = models.TextField()  # This field type is a guess.
    guest_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'guest_user'


class MasterConfig(models.Model):
    key = models.CharField(max_length=200, blank=True, null=True)
    value = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'master_config'


class MasterData(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=500)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=1024, blank=True, null=True)
    extend = models.CharField(max_length=1024, blank=True, null=True)
    # This field type is a guess.
    option = models.TextField(blank=True, null=True)
    group_id = models.IntegerField()
    theme_id = models.CharField(max_length=50, blank=True, null=True)
    menu_count = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_data'


class MasterDataGroup(models.Model):
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    extend = models.CharField(max_length=1024, blank=True, null=True)
    # This field type is a guess.
    option = models.TextField(blank=True, null=True)
    enabled = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_data_group'


class MasterLanguage(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    html_name = models.CharField(max_length=200, blank=True, null=True)
    ja = models.CharField(max_length=200, blank=True, null=True)
    en = models.CharField(max_length=200, blank=True, null=True)
    zh = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_language'


class Menu(models.Model):
    no = models.IntegerField()
    name = models.CharField(max_length=200, blank=True, null=True)
    usable = models.BooleanField()
    price = models.DecimalField(max_digits=8, decimal_places=0)
    note = models.CharField(max_length=200, blank=True, null=True)
    stock_status_id = models.IntegerField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    tax_in = models.BooleanField()
    ori_price = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu'


class MenuBind(models.Model):
    menu_id = models.IntegerField(primary_key=True)
    bind_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_bind'


class MenuCategory(models.Model):
    display_order = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    menu_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_category'


class MenuComment(models.Model):
    good = models.BooleanField(blank=True, null=True)
    comment = models.TextField()
    time = models.DateTimeField()
    guest_id = models.IntegerField()
    menu_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu_comment'


class MenuCourse(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    count = models.IntegerField()
    display_order = models.IntegerField()
    usable_time = models.IntegerField()
    cancel_possible = models.IntegerField()
    menu_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField()
    tax_in = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'menu_course'


class MenuCourseDetail(models.Model):
    menu_id = models.IntegerField(blank=True, null=True)
    menu_course_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_course_detail'


class MenuFree(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    usable_time = models.IntegerField()
    display_order = models.IntegerField()
    free_type_id = models.IntegerField(blank=True, null=True)
    menu_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_free'


class MenuFreeDetail(models.Model):
    menu_id = models.IntegerField(blank=True, null=True)
    menu_free_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_free_detail'


class MenuOption(models.Model):
    icon = models.CharField(max_length=200, blank=True, null=True)
    display_order = models.IntegerField()
    data_id = models.IntegerField(blank=True, null=True)
    menu_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu_option'


class MenuSale(models.Model):
    is_all = models.BooleanField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    ratio = models.DecimalField(max_digits=8, decimal_places=2)
    is_infinite = models.BooleanField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    max_count = models.IntegerField()
    menu_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu_sale'


class MenuTop(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    target_type = models.CharField(max_length=20, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    sort = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    enabled = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    option = models.TextField(blank=True, null=True)
    menu_type = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'menu_top'


class MstIngredients(models.Model):
    ing_no = models.CharField(max_length=16, blank=True, null=True)
    ing_name = models.CharField(max_length=64, blank=True, null=True)
    ing_cat_id = models.IntegerField(blank=True, null=True)
    stock_unit = models.CharField(max_length=8, blank=True, null=True)
    consumption_unit = models.CharField(max_length=8, blank=True, null=True)
    unit_conv_rate = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    ave_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(
        max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_ingredients'


class MstIngredientsCat(models.Model):
    cat_no = models.IntegerField(blank=True, null=True)
    cat_name = models.CharField(max_length=32, blank=True, null=True)
    explanation = models.CharField(max_length=64, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    hierarchy_path = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(
        max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_ingredients_cat'


class Order(models.Model):
    order_no = models.CharField(max_length=20)
    counter_no = models.CharField(max_length=64)
    order_time = models.DateTimeField()
    guest_id = models.IntegerField(blank=True, null=True)
    order_method_id = models.IntegerField(blank=True, null=True)
    order_type_id = models.IntegerField(blank=True, null=True)
    seat_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class OrderDetail(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=0)
    # This field type is a guess.
    option = models.TextField(blank=True, null=True)
    count = models.IntegerField()
    cancelable = models.BooleanField(blank=True, null=True)
    menu_id = models.IntegerField()
    order_id = models.IntegerField()
    ori_price = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail'


class OrderDetailHistory(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=0)
    # This field type is a guess.
    option = models.TextField(blank=True, null=True)
    count = models.IntegerField()
    cancelable = models.BooleanField(blank=True, null=True)
    menu_id = models.IntegerField()
    order_id = models.IntegerField()
    ori_price = models.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail_history'


class OrderDetailMenuFree(models.Model):
    usable = models.BooleanField()
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    stop = models.DateTimeField(blank=True, null=True)
    menu_free_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField()
    order_detail_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_detail_menu_free'


class OrderDetailMenuFreeHistory(models.Model):
    usable = models.BooleanField()
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    stop = models.DateTimeField(blank=True, null=True)
    menu_free_id = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField()
    order_detail_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_detail_menu_free_history'


class OrderDetailStatus(models.Model):
    start_time = models.DateTimeField()
    current = models.BooleanField(blank=True, null=True)
    order_detail_id = models.IntegerField()
    status_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail_status'


class OrderDetailStatusHistory(models.Model):
    start_time = models.DateTimeField()
    current = models.BooleanField(blank=True, null=True)
    order_detail_id = models.IntegerField()
    status_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail_status_history'


class OrderHistory(models.Model):
    order_no = models.CharField(max_length=20)
    counter_no = models.CharField(max_length=64)
    order_time = models.DateTimeField()
    guest_id = models.IntegerField(blank=True, null=True)
    order_method_id = models.IntegerField(blank=True, null=True)
    order_type_id = models.IntegerField(blank=True, null=True)
    seat_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_history'


class Reservation(models.Model):
    reservation_no = models.CharField(max_length=64)
    name = models.CharField(max_length=100, blank=True, null=True)
    tel = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    reservation_time = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    counter_no = models.CharField(max_length=64)
    enter_time = models.DateTimeField(blank=True, null=True)
    # Field name made lowercase.
    reservation_type_id = models.IntegerField(db_column='Reservation_type_id')
    guest_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation'


class ReservationDetail(models.Model):
    # Field name made lowercase.
    seat_id = models.IntegerField(db_column='Seat_id')
    reservation_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation_detail'


class ReservationHistory(models.Model):
    reservation_no = models.CharField(max_length=64)
    # Field name made lowercase. This field type is a guess.
    reservation = models.TextField(db_column='Reservation')
    # Field name made lowercase. This field type is a guess.
    reservationdetail = models.TextField(db_column='ReservationDetail')

    class Meta:
        managed = False
        db_table = 'reservation_history'


class ReservationMenu(models.Model):
    menu_id = models.IntegerField(blank=True, null=True)
    reservation_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation_menu'


class Role(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    level = models.IntegerField()
    display_name = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'


class RoleDetail(models.Model):
    view = models.CharField(max_length=200, blank=True, null=True)
    action = models.CharField(max_length=20, blank=True, null=True)
    role_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'role_detail'


class RoleUser(models.Model):
    note = models.CharField(max_length=200, blank=True, null=True)
    role_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'role_user'


class Seat(models.Model):
    seat_no = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    start = models.DateTimeField(blank=True, null=True)
    usable = models.BooleanField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    group_id = models.IntegerField()
    seat_smoke_type_id = models.IntegerField(blank=True, null=True)
    seat_type_id = models.IntegerField(blank=True, null=True)
    takeout_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat'


class SeatFree(models.Model):
    seat_id = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    menu_free_id = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    status = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat_free'


class SeatGroup(models.Model):
    no = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    start = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat_group'


class SeatStatus(models.Model):
    counter_no = models.CharField(max_length=64)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    security_key = models.CharField(max_length=256)
    seat_id = models.IntegerField()
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat_status'


class SeatStatusHistory(models.Model):
    counter_no = models.CharField(max_length=64)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    security_key = models.CharField(max_length=256)
    seat_id = models.IntegerField()
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat_status_history'


class SeatUser(models.Model):
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    guest_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'seat_user'


class SeatUserHistory(models.Model):
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    guest_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'seat_user_history'


class Takeout(models.Model):
    counter_no = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'takeout'


class TblRecipe(models.Model):
    ing_id = models.IntegerField(blank=True, null=True)
    serving = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    amount_to_use = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    menu_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_recipe'

class TakeoutUser(models.Model):
    user_name = models.CharField( max_length=100)
    user_tel = models.CharField(max_length=100)
    user_address = models.CharField( max_length=200)
    seat_no = models.IntegerField(blank=True)
    create_time = models.DateTimeField()
    user_id = models.CharField(max_length=100)
    user_pass = models.CharField(max_length=128)
    user_email = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'takeout_user'

class TakeoutOrder(models.Model):
    ship_addr = models.CharField(max_length=200, blank=True, null=True)
    ship_time = models.DateTimeField(blank=True, null=True)
    ship_tel = models.CharField(max_length=100, blank=True, null=True)
    pay_type = models.IntegerField(blank=True, null=True)
    pay_status = DjangoModel.IntegerField(blank=True, null=True)
    order_status = DjangoModel.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    ship_name = models.CharField(max_length=30, blank=True, null=True)
    delivery_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'takeout_order'

class TakeoutOrderDetail(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    menu_id = models.IntegerField(blank=True, null=True)
    menu_id = models.IntegerField(blank=True, null=True)
    menu_name = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'takeout_order_detail'