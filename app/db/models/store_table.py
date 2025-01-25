
from django.db import models as DjangoModel
from app.db.models.base import BaseModel
from django.contrib.postgres.fields import JSONField


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
    tax = DjangoModel.DecimalField(
        max_digits=3, decimal_places=0, blank=True, null=True)
    total = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    price = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    pay = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    change = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    cut = DjangoModel.DecimalField(
        max_digits=3, decimal_places=0, blank=True, null=True)
    reduce = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    canceled = DjangoModel.BooleanField(blank=True, null=True)
    create_time = DjangoModel.DateTimeField()
    canceled_type_id = DjangoModel.IntegerField(blank=True, null=True)
    counter_id = DjangoModel.IntegerField(blank=True, null=True)
    pay_method_id = DjangoModel.IntegerField(blank=True, null=True)
    user_id = DjangoModel.IntegerField(blank=True, null=True)
    amounts_actually = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    amounts_actually_tax = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    amounts_payable = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    cut_value = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    price_tax_in = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    tax_value = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

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
    pay_price = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    tax_in = DjangoModel.BooleanField()
    ori_price = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

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


class Guest(BaseModel):
    no = DjangoModel.IntegerField(blank=True, null=True)
    nickname = DjangoModel.CharField(max_length=100, blank=True, null=True)
    sur_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    given_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    sur_name_fricana = DjangoModel.CharField(
        max_length=100, blank=True, null=True)
    given_name_fricana = DjangoModel.CharField(
        max_length=100, blank=True, null=True)
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
    settings = JSONField(null=True, blank=True)
    guest_id = DjangoModel.IntegerField()
    user_id = DjangoModel.IntegerField()

    class Meta:
        managed = False
        db_table = 'guest_user'


class MasterConfig(BaseModel):
    key = DjangoModel.CharField(max_length=200, blank=True, null=True)
    value = JSONField(null=True, blank=True)

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
    option = JSONField(null=True, blank=True)
    group_id = DjangoModel.IntegerField()
    theme_id = DjangoModel.CharField(max_length=50, blank=True, null=True)
    menu_count = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

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
    option = JSONField(null=True, blank=True)
    enabled = DjangoModel.IntegerField(default=1)

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
    ori_price = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)
    image = DjangoModel.TextField(blank=True, null=True)
    updated_at = DjangoModel.DateTimeField(auto_now=True)
    takeout = DjangoModel.IntegerField(blank=True, null=True)
    mincount = DjangoModel.DecimalField(max_digits=8, decimal_places=0)

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
    price = DjangoModel.IntegerField()

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
    sort = DjangoModel.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    enabled = DjangoModel.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    menu_type = DjangoModel.CharField(max_length=20, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'menu_top'


class MstIngredients(BaseModel):
    ing_no = DjangoModel.CharField(max_length=16, blank=True, null=True)
    ing_name = DjangoModel.CharField(max_length=64, blank=True, null=True)
    ing_cat_id = DjangoModel.IntegerField(blank=True, null=True)
    stock_unit = DjangoModel.CharField(max_length=8, blank=True, null=True)
    consumption_unit = DjangoModel.CharField(
        max_length=8, blank=True, null=True)
    unit_conv_rate = DjangoModel.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    ave_price = DjangoModel.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_ingredients'


class MstIngredientsCat(BaseModel):
    cat_no = DjangoModel.IntegerField(blank=True, null=True)
    cat_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    explanation = DjangoModel.CharField(max_length=64, blank=True, null=True)
    parent_id = DjangoModel.IntegerField(blank=True, null=True)
    hierarchy_path = DjangoModel.CharField(
        max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_ingredients_cat'


class ShopCost(BaseModel):
    cost_name = DjangoModel.CharField(max_length=64, blank=True, null=True)
    cost_category_id = DjangoModel.IntegerField(blank=True, null=True)
    pay_time = DjangoModel.DateTimeField(blank=True, null=True)
    cost = DjangoModel.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_cost'


class ShopCostCat(BaseModel):
    category_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    parent_id = DjangoModel.IntegerField(blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_cost_category'


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
    option = JSONField(null=True, blank=True)
    count = DjangoModel.IntegerField()
    cancelable = DjangoModel.BooleanField(blank=True, null=True)
    menu_id = DjangoModel.IntegerField()
    order_id = DjangoModel.IntegerField()
    ori_price = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail'


class OrderDetailHistory(BaseModel):
    price = DjangoModel.DecimalField(max_digits=8, decimal_places=0)
    option = JSONField(null=True, blank=True)
    count = DjangoModel.IntegerField()
    cancelable = DjangoModel.BooleanField(blank=True, null=True)
    menu_id = DjangoModel.IntegerField()
    order_id = DjangoModel.IntegerField()
    ori_price = DjangoModel.DecimalField(
        max_digits=8, decimal_places=0, blank=True, null=True)

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
    # Field name made lowercase.
    reservation_type_id = DjangoModel.IntegerField(
        db_column='Reservation_type_id')
    guest_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation'


class ReservationDetail(BaseModel):
    # Field name made lowercase.
    seat_id = DjangoModel.IntegerField(db_column='Seat_id')
    reservation_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservation_detail'


class ReservationHistory(BaseModel):
    reservation_no = DjangoModel.CharField(max_length=64)
    # Field name made lowercase. This field type is a guess.
    reservation = DjangoModel.TextField(db_column='Reservation')
    # Field name made lowercase. This field type is a guess.
    reservationdetail = DjangoModel.TextField(db_column='ReservationDetail')

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
    takeout_type = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat'


class SeatFree(BaseModel):
    seat_id = DjangoModel.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    menu_free_id = DjangoModel.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    start = DjangoModel.DateTimeField(blank=True, null=True)
    status = DjangoModel.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seat_free'


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


class TblRecipe(BaseModel):
    ing_id = DjangoModel.IntegerField(blank=True, null=True)
    serving = DjangoModel.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    amount_to_use = DjangoModel.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    menu_id = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_recipe'


class AuthUser(BaseModel):
    password = DjangoModel.CharField(max_length=128)
    last_login = DjangoModel.DateTimeField(blank=True, null=True)
    is_superuser = DjangoModel.BooleanField()
    username = DjangoModel.CharField(unique=True, max_length=150)
    first_name = DjangoModel.CharField(max_length=30)
    last_name = DjangoModel.CharField(max_length=150)
    email = DjangoModel.CharField(max_length=254)
    is_staff = DjangoModel.BooleanField()
    is_active = DjangoModel.BooleanField()
    date_joined = DjangoModel.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthGroup(BaseModel):
    name = DjangoModel.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthUserGroups(BaseModel):
    user = DjangoModel.ForeignKey(AuthUser, DjangoModel.DO_NOTHING)
    group = DjangoModel.ForeignKey(AuthGroup, DjangoModel.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthMenu(BaseModel):
    menu_path = DjangoModel.CharField(unique=True, max_length=80)
    group_id = DjangoModel.IntegerField(blank=True)

    class Meta:
        managed = False
        db_table = 'auth_menu'


class Machine(BaseModel):
    sign = DjangoModel.CharField(unique=True, max_length=128)
    update_data = DjangoModel.DateTimeField()
    status = DjangoModel.BooleanField()
    last_data = DjangoModel.DateTimeField()

    class Meta:
        managed = False
        db_table = 'machine'

class TakeoutUser(BaseModel):
    user_name = DjangoModel.CharField( max_length=100)
    user_tel = DjangoModel.CharField( max_length=100)
    user_address = DjangoModel.CharField( max_length=200)
    seat_no = DjangoModel.IntegerField(blank=True)
    create_time = DjangoModel.DateTimeField()
    user_id = DjangoModel.CharField(max_length=100)
    user_pass = DjangoModel.CharField(max_length=128)
    user_email = DjangoModel.CharField(max_length=100)


    class Meta:
        managed = False
        db_table = 'takeout_user'



class TakeoutOrder(BaseModel):
    ship_addr = DjangoModel.CharField(max_length=200, blank=True, null=True)
    ship_time = DjangoModel.DateTimeField(blank=True, null=True)
    ship_tel = DjangoModel.CharField(max_length=100, blank=True, null=True)
    pay_type = DjangoModel.IntegerField(blank=True, null=True)
    pay_status = DjangoModel.IntegerField(blank=True, null=True)
    order_status = DjangoModel.IntegerField(blank=True, null=True)
    user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_time = DjangoModel.DateTimeField(blank=True, null=True)
    ship_name = DjangoModel.CharField(max_length=30, blank=True, null=True)
    delivery_type = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'takeout_order'

class TakeoutOrderDetail(BaseModel):
    order_id = DjangoModel.IntegerField(blank=True, null=True)
    menu_id = DjangoModel.IntegerField(blank=True, null=True)
    menu_id = DjangoModel.IntegerField(blank=True, null=True)
    menu_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    price = DjangoModel.CharField(max_length=100, blank=True, null=True)
    count = DjangoModel.IntegerField(blank=True, null=True)
    create_time = DjangoModel.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'takeout_order_detail'

class ProfitInventory(BaseModel):
    inventory_date = DjangoModel.DateTimeField(blank=True, null=True)
    inventory_user = DjangoModel.CharField(max_length=32, blank=True, null=True)
    status = DjangoModel.IntegerField(blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profit_inventory'

class ProfitInventoryDetail(BaseModel):
    inventory_id = DjangoModel.IntegerField(blank=True, null=True)
    inventory_date = DjangoModel.DateTimeField(blank=True, null=True)
    part_id = DjangoModel.IntegerField(blank=True, null=True)
    parts_type = DjangoModel.CharField(max_length=32, blank=True, null=True)
    part_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    parts_inventory_qty = DjangoModel.IntegerField(blank=True, null=True)
    parts_inventory_actual = DjangoModel.IntegerField(blank=True, null=True)
    ave_price = DjangoModel.IntegerField(blank=True, null=True)
    remarks = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(
        max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profit_inventory_detail'