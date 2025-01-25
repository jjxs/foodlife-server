# OrderDetail.objects.using('ami').create(
#     price = 9999999,
#     count = 9999999,
#     menu_id = 9999999,
#     order_id = 9999999)
# detail.insert()
from django.db import models as DjangoModel
from app.db.models.base import BaseModel

class Counter(BaseModel):
    is_pay = DjangoModel.BooleanField(blank=True, null=True)
    is_split = DjangoModel.BooleanField(blank=True, null=True)
    is_average = DjangoModel.BooleanField(blank=True, null=True)
    is_input = DjangoModel.BooleanField(blank=True, null=True)
    number = DjangoModel.IntegerField()
    create_time = DjangoModel.DateTimeField()
    delete = DjangoModel.BooleanField(blank=True, null=True)
    delete_type_id = DjangoModel.IntegerField(blank=True, null=True)
    user_id = DjangoModel.IntegerField(blank=True, null=True)
    is_completed = DjangoModel.BooleanField(blank=True, null=True)
    pay_price = DjangoModel.IntegerField()
    tax_price = DjangoModel.IntegerField()
    total_price = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'counter'


class CounterDetail(BaseModel):
    no = DjangoModel.CharField(max_length=64, blank=True, null=True)
    tax = DjangoModel.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    total = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    price = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    pay = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    change = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    cut = DjangoModel.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    reduce = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    canceled = DjangoModel.BooleanField(blank=True, null=True)
    create_time = DjangoModel.DateTimeField()
    canceled_type_id = DjangoModel.IntegerField(blank=True, null=True)
    counter_id = DjangoModel.IntegerField(blank=True, null=True)
    pay_method_id = DjangoModel.IntegerField(blank=True, null=True)
    user_id = DjangoModel.IntegerField(blank=True, null=True)
    amounts_actually = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    amounts_actually_tax = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    amounts_payable = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    cut_value = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    price_tax_in = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    tax_value = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'counter_detail'


class CounterDetailOrder(BaseModel):
    order_detail_id = DjangoModel.IntegerField()
    pay_count = DjangoModel.IntegerField()
    is_delete = DjangoModel.BooleanField(blank=True, null=True)
    is_ready = DjangoModel.BooleanField(blank=True, null=True)
    is_split = DjangoModel.BooleanField(blank=True, null=True)
    counter_id = DjangoModel.IntegerField(blank=True, null=True)
    counter_detail_id = DjangoModel.IntegerField(blank=True, null=True)
    pay_price = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    tax_in = DjangoModel.BooleanField()
    ori_price = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'counter_detail_order'


class CounterSeat(BaseModel):
    seat_id = DjangoModel.IntegerField()
    seat_status_id = DjangoModel.IntegerField()
    counter_no = DjangoModel.CharField(max_length=64)
    counter_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'counter_seat'


class DjangoContentType(BaseModel):
    app_label = DjangoModel.CharField(max_length=100)
    model = DjangoModel.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(BaseModel):
    app = DjangoModel.CharField(max_length=255)
    name = DjangoModel.CharField(max_length=255)
    applied = DjangoModel.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(BaseModel):
    session_key = DjangoModel.CharField(primary_key=True, max_length=40)
    session_data = DjangoModel.TextField()
    expire_date = DjangoModel.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Guest(BaseModel):
    no = DjangoModel.IntegerField(blank=True, null=True)
    nickname = DjangoModel.CharField(max_length=100, blank=True, null=True)
    sur_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    given_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    sur_name_fricana = DjangoModel.CharField(max_length=100, blank=True, null=True)
    given_name_fricana = DjangoModel.CharField(max_length=100, blank=True, null=True)
    birthday = DjangoModel.DateField(blank=True, null=True)
    sex = DjangoModel.IntegerField(blank=True, null=True)
    tel = DjangoModel.CharField(max_length=30, blank=True, null=True)
    phone = DjangoModel.CharField(max_length=30, blank=True, null=True)
    married = DjangoModel.BooleanField(blank=True, null=True)
    created = DjangoModel.DateTimeField()
    is_temporary = DjangoModel.BooleanField(blank=True, null=True)
    final_education_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest'


class GuestDevice(BaseModel):
    device_id = DjangoModel.CharField(max_length=512)
    device_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    note = DjangoModel.CharField(max_length=1024, blank=True, null=True)
    created = DjangoModel.DateTimeField()
    device_type_id = DjangoModel.IntegerField(blank=True, null=True)
    guest_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'guest_device'


class GuestGroup(BaseModel):
    name = DjangoModel.CharField(max_length=200)
    evel_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest_group'


class GuestGroupDetail(BaseModel):
    guest_id = DjangoModel.IntegerField()
    guestgroup_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'guest_group_detail'


class GuestUser(BaseModel):
    display_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    created = DjangoModel.DateTimeField()
    settings = DjangoModel.TextField()  # This field type is a guess.
    guest_id = DjangoModel.IntegerField()
    user_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'guest_user'


class MasterConfig(BaseModel):
    key = DjangoModel.CharField(max_length=200, blank=True, null=True)
    value = DjangoModel.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'master_config'


class MasterData(BaseModel):
    code = DjangoModel.IntegerField()
    name = DjangoModel.CharField(max_length=500)
    display_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    display_order = DjangoModel.IntegerField(blank=True, null=True)
    note = DjangoModel.CharField(max_length=1024, blank=True, null=True)
    extend = DjangoModel.CharField(max_length=1024, blank=True, null=True)
    option = DjangoModel.TextField(blank=True, null=True)  # This field type is a guess.
    group_id = DjangoModel.IntegerField()
    theme_id = DjangoModel.CharField(max_length=50, blank=True, null=True)
    menu_count = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_data'


class MasterDataGroup(BaseModel):
    name = DjangoModel.CharField(max_length=200)
    display_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    domain = DjangoModel.CharField(max_length=100, blank=True, null=True)
    note = DjangoModel.CharField(max_length=200, blank=True, null=True)
    display_order = DjangoModel.IntegerField(blank=True, null=True)
    extend = DjangoModel.CharField(max_length=1024, blank=True, null=True)
    option = DjangoModel.TextField(blank=True, null=True)  # This field type is a guess.
    enabled = DjangoModel.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_data_group'


class MasterLanguage(BaseModel):
    name = DjangoModel.CharField(max_length=200, blank=True, null=True)
    html_name = DjangoModel.CharField(max_length=200, blank=True, null=True)
    ja = DjangoModel.CharField(max_length=200, blank=True, null=True)
    en = DjangoModel.CharField(max_length=200, blank=True, null=True)
    zh = DjangoModel.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_language'


class Menu(BaseModel):
    no = DjangoModel.IntegerField()
    name = DjangoModel.CharField(max_length=200, blank=True, null=True)
    usable = DjangoModel.BooleanField()
    price = DjangoModel.DecimalField(max_digits=8, decimal_places=0)
    note = DjangoModel.CharField(max_length=200, blank=True, null=True)
    stock_status_id = DjangoModel.IntegerField(blank=True, null=True)
    introduction = DjangoModel.TextField(blank=True, null=True)
    tax_in = DjangoModel.BooleanField()
    ori_price = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu'


class MenuCategory(BaseModel):
    display_order = DjangoModel.IntegerField(blank=True, null=True)
    category_id = DjangoModel.IntegerField(blank=True, null=True)
    menu_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_category'


class MenuComment(BaseModel):
    good = DjangoModel.BooleanField(blank=True, null=True)
    comment = DjangoModel.TextField()
    time = DjangoModel.DateTimeField()
    guest_id = DjangoModel.IntegerField()
    menu_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu_comment'


class MenuCourse(BaseModel):
    name = DjangoModel.CharField(max_length=200, blank=True, null=True)
    price = DjangoModel.DecimalField(max_digits=8, decimal_places=0)
    count = DjangoModel.IntegerField()
    display_order = DjangoModel.IntegerField()
    usable_time = DjangoModel.IntegerField()
    cancel_possible = DjangoModel.IntegerField()
    menu_id = DjangoModel.IntegerField(blank=True, null=True)
    level = DjangoModel.IntegerField()
    tax_in = DjangoModel.BooleanField()

    class Meta:
        managed = False
        db_table = 'menu_course'


class MenuCourseDetail(BaseModel):
    menu_id = DjangoModel.IntegerField(blank=True, null=True)
    menu_course_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_course_detail'


class MenuFree(BaseModel):
    name = DjangoModel.CharField(max_length=200, blank=True, null=True)
    usable_time = DjangoModel.IntegerField()
    display_order = DjangoModel.IntegerField()
    free_type_id = DjangoModel.IntegerField(blank=True, null=True)
    menu_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_free'


class MenuFreeDetail(BaseModel):
    menu_id = DjangoModel.IntegerField(blank=True, null=True)
    menu_free_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_free_detail'


class MenuOption(BaseModel):
    icon = DjangoModel.CharField(max_length=200, blank=True, null=True)
    display_order = DjangoModel.IntegerField()
    data_id = DjangoModel.IntegerField(blank=True, null=True)
    menu_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu_option'


class MenuSale(BaseModel):
    is_all = DjangoModel.BooleanField(blank=True, null=True)
    price = DjangoModel.DecimalField(max_digits=8, decimal_places=0)
    ratio = DjangoModel.DecimalField(max_digits=8, decimal_places=2)
    is_infinite = DjangoModel.BooleanField(blank=True, null=True)
    start = DjangoModel.DateTimeField(blank=True, null=True)
    end = DjangoModel.DateTimeField(blank=True, null=True)
    max_count = DjangoModel.IntegerField()
    menu_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu_sale'


class MenuTop(BaseModel):
    name = DjangoModel.CharField(max_length=20, blank=True, null=True)
    target_type = DjangoModel.CharField(max_length=20, blank=True, null=True)
    link = DjangoModel.CharField(max_length=200, blank=True, null=True)
    image = DjangoModel.CharField(max_length=200, blank=True, null=True)
    note = DjangoModel.CharField(max_length=200, blank=True, null=True)
    sort = DjangoModel.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    enabled = DjangoModel.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_top'


class Order(BaseModel):
    order_no = DjangoModel.CharField(max_length=20)
    counter_no = DjangoModel.CharField(max_length=64)
    order_time = DjangoModel.DateTimeField()
    guest_id = DjangoModel.IntegerField(blank=True, null=True)
    order_method_id = DjangoModel.IntegerField(blank=True, null=True)
    order_type_id = DjangoModel.IntegerField(blank=True, null=True)
    seat_id = DjangoModel.IntegerField(blank=True, null=True)
    user_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class OrderDetail(BaseModel):
    price = DjangoModel.DecimalField(max_digits=8, decimal_places=0)
    option = DjangoModel.TextField(blank=True, null=True)  # This field type is a guess.
    count = DjangoModel.IntegerField()
    cancelable = DjangoModel.BooleanField(blank=True, null=True)
    menu_id = DjangoModel.IntegerField()
    order_id = DjangoModel.IntegerField()
    ori_price = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail'


class OrderDetailHistory(BaseModel):
    price = DjangoModel.DecimalField(max_digits=8, decimal_places=0)
    option = DjangoModel.TextField(blank=True, null=True)  # This field type is a guess.
    count = DjangoModel.IntegerField()
    cancelable = DjangoModel.BooleanField(blank=True, null=True)
    menu_id = DjangoModel.IntegerField()
    order_id = DjangoModel.IntegerField()
    ori_price = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail_history'


class OrderDetailMenuFree(BaseModel):
    usable = DjangoModel.BooleanField()
    start = DjangoModel.DateTimeField(blank=True, null=True)
    end = DjangoModel.DateTimeField(blank=True, null=True)
    stop = DjangoModel.DateTimeField(blank=True, null=True)
    menu_free_id = DjangoModel.IntegerField(blank=True, null=True)
    order_id = DjangoModel.IntegerField()
    order_detail_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_detail_menu_free'


class OrderDetailMenuFreeHistory(BaseModel):
    usable = DjangoModel.BooleanField()
    start = DjangoModel.DateTimeField(blank=True, null=True)
    end = DjangoModel.DateTimeField(blank=True, null=True)
    stop = DjangoModel.DateTimeField(blank=True, null=True)
    menu_free_id = DjangoModel.IntegerField(blank=True, null=True)
    order_id = DjangoModel.IntegerField()
    order_detail_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_detail_menu_free_history'


class OrderDetailStatus(BaseModel):
    start_time = DjangoModel.DateTimeField()
    current = DjangoModel.BooleanField(blank=True, null=True)
    order_detail_id = DjangoModel.IntegerField()
    status_id = DjangoModel.IntegerField(blank=True, null=True)
    user_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail_status'


class OrderDetailStatusHistory(BaseModel):
    start_time = DjangoModel.DateTimeField()
    current = DjangoModel.BooleanField(blank=True, null=True)
    order_detail_id = DjangoModel.IntegerField()
    status_id = DjangoModel.IntegerField(blank=True, null=True)
    user_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail_status_history'


class OrderHistory(BaseModel):
    order_no = DjangoModel.CharField(max_length=20)
    counter_no = DjangoModel.CharField(max_length=64)
    order_time = DjangoModel.DateTimeField()
    guest_id = DjangoModel.IntegerField(blank=True, null=True)
    order_method_id = DjangoModel.IntegerField(blank=True, null=True)
    order_type_id = DjangoModel.IntegerField(blank=True, null=True)
    seat_id = DjangoModel.IntegerField(blank=True, null=True)
    user_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_history'


class Reservation(BaseModel):
    reservation_no = DjangoModel.CharField(max_length=64)
    name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    tel = DjangoModel.CharField(max_length=30, blank=True, null=True)
    phone = DjangoModel.CharField(max_length=30, blank=True, null=True)
    reservation_time = DjangoModel.DateTimeField(blank=True, null=True)
    number = DjangoModel.IntegerField(blank=True, null=True)
    counter_no = DjangoModel.CharField(max_length=64)
    enter_time = DjangoModel.DateTimeField(blank=True, null=True)
    reservation_type_id = DjangoModel.IntegerField(db_column='Reservation_type_id')  # Field name made lowercase.
    guest_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation'


class ReservationDetail(BaseModel):
    seat_id = DjangoModel.IntegerField(db_column='Seat_id')  # Field name made lowercase.
    reservation_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation_detail'


class ReservationHistory(BaseModel):
    reservation_no = DjangoModel.CharField(max_length=64)
    reservation = DjangoModel.TextField(db_column='Reservation')  # Field name made lowercase. This field type is a guess.
    reservationdetail = DjangoModel.TextField(db_column='ReservationDetail')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'reservation_history'


class ReservationMenu(BaseModel):
    menu_id = DjangoModel.IntegerField(blank=True, null=True)
    reservation_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation_menu'


class Role(BaseModel):
    name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    level = DjangoModel.IntegerField()
    display_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    note = DjangoModel.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'


class RoleDetail(BaseModel):
    view = DjangoModel.CharField(max_length=200, blank=True, null=True)
    action = DjangoModel.CharField(max_length=20, blank=True, null=True)
    role_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'role_detail'


class RoleUser(BaseModel):
    note = DjangoModel.CharField(max_length=200, blank=True, null=True)
    role_id = DjangoModel.IntegerField()
    user_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'role_user'


class Seat(BaseModel):
    seat_no = DjangoModel.CharField(max_length=20)
    name = DjangoModel.CharField(max_length=200)
    start = DjangoModel.DateTimeField(blank=True, null=True)
    usable = DjangoModel.BooleanField(blank=True, null=True)
    number = DjangoModel.IntegerField(blank=True, null=True)
    group_id = DjangoModel.IntegerField()
    seat_smoke_type_id = DjangoModel.IntegerField(blank=True, null=True)
    seat_type_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat'


class SeatGroup(BaseModel):
    no = DjangoModel.CharField(max_length=20)
    name = DjangoModel.CharField(max_length=200)
    start = DjangoModel.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat_group'


class SeatStatus(BaseModel):
    counter_no = DjangoModel.CharField(max_length=64)
    start = DjangoModel.DateTimeField(blank=True, null=True)
    end = DjangoModel.DateTimeField(blank=True, null=True)
    security_key = DjangoModel.CharField(max_length=256)
    seat_id = DjangoModel.IntegerField()
    number = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat_status'


class SeatStatusHistory(BaseModel):
    counter_no = DjangoModel.CharField(max_length=64)
    start = DjangoModel.DateTimeField(blank=True, null=True)
    end = DjangoModel.DateTimeField(blank=True, null=True)
    security_key = DjangoModel.CharField(max_length=256)
    seat_id = DjangoModel.IntegerField()
    number = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat_status_history'


class SeatUser(BaseModel):
    start = DjangoModel.DateTimeField(blank=True, null=True)
    end = DjangoModel.DateTimeField(blank=True, null=True)
    guest_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'seat_user'


class SeatUserHistory(BaseModel):
    start = DjangoModel.DateTimeField(blank=True, null=True)
    end = DjangoModel.DateTimeField(blank=True, null=True)
    guest_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'seat_user_history'


class Takeout(BaseModel):
    counter_no = DjangoModel.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'takeout'
