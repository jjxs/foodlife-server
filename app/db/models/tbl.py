
from django.db import models as DjangoModel
from app.db.models.base import BaseModel
from django.contrib.postgres.fields import JSONField


class TblAttRecord(BaseModel):
    working_day = DjangoModel.DateField(blank=True, null=True)
    attendance_time = DjangoModel.DateTimeField(blank=True, null=True)
    leaving_time = DjangoModel.DateTimeField(blank=True, null=True)
    working_time = DjangoModel.CharField(max_length=8, blank=True, null=True)
    break_time = DjangoModel.CharField(max_length=8, blank=True, null=True)
    late_time = DjangoModel.CharField(max_length=8, blank=True, null=True)
    leave_early_time = DjangoModel.CharField(max_length=8, blank=True, null=True)
    midnight_working_hours = DjangoModel.CharField(max_length=8, blank=True, null=True)
    holiday_working_hours = DjangoModel.CharField(max_length=8, blank=True, null=True)
    attendance_category = DjangoModel.IntegerField(blank=True, null=True)
    emp_id = DjangoModel.IntegerField(blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_att_record'


class TblAttendance(BaseModel):
    working_day = DjangoModel.DateField(blank=True, null=True)
    time_division = DjangoModel.IntegerField(blank=True, null=True)
    punch_time = DjangoModel.DateTimeField(blank=True, null=True)
    emp_id = DjangoModel.IntegerField(blank=True, null=True)
    place = DjangoModel.TextField(blank=True, null=True)  # This field type is a guess.
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_attendance'


class TblHolidayDef(BaseModel):
    holiday_class = DjangoModel.CharField(max_length=8, blank=True, null=True)
    date = DjangoModel.DateField(blank=True, null=True)
    name = DjangoModel.CharField(max_length=512, blank=True, null=True)
    authority_id = DjangoModel.IntegerField(blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_holiday_def'


class TblInspection(BaseModel):
    part_id = DjangoModel.IntegerField(blank=True, null=True)
    part_cat = DjangoModel.IntegerField(blank=True, null=True)
    part_type = DjangoModel.IntegerField(blank=True, null=True)
    part_unit = DjangoModel.CharField(max_length=16, blank=True, null=True)
    parts_unit_price = DjangoModel.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    parts_currency = DjangoModel.CharField(max_length=16, blank=True, null=True)
    parts_inventory_qty = DjangoModel.IntegerField(blank=True, null=True)
    inspection_date = DjangoModel.DateTimeField(blank=True, null=True)
    inspector = DjangoModel.CharField(max_length=16, blank=True, null=True)
    inspection_result_confirmation = DjangoModel.CharField(max_length=8, blank=True, null=True)
    remarks = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    inspection_delete = DjangoModel.IntegerField(blank=True, null=True)
    base = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_inspection'


class TblIssue(BaseModel):
    goods_issue_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    part_id = DjangoModel.IntegerField(blank=True, null=True)
    base = DjangoModel.CharField(max_length=32, blank=True, null=True)
    issue_date = DjangoModel.DateField(blank=True, null=True)
    goods_issue_quantity = DjangoModel.CharField(max_length=16, blank=True, null=True)
    delivery_status_checker = DjangoModel.CharField(max_length=16, blank=True, null=True)
    goods_issue_indicator = DjangoModel.IntegerField(blank=True, null=True)
    remarks = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_issue'


class TblOrder(BaseModel):
    order_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    orderer = DjangoModel.CharField(max_length=16, blank=True, null=True)
    order_date = DjangoModel.DateField(blank=True, null=True)
    order_address = DjangoModel.CharField(max_length=128, blank=True, null=True)
    order_phone_number = DjangoModel.IntegerField(blank=True, null=True)
    order_summary = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    base = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_order'


class TblOrderDetail(BaseModel):
    ordering_table_unique_id = DjangoModel.IntegerField(blank=True, null=True)
    part_id = DjangoModel.IntegerField(blank=True, null=True)
    part_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    parts_type = DjangoModel.CharField(max_length=8, blank=True, null=True)
    parts_unit_price = DjangoModel.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    parts_currency = DjangoModel.CharField(max_length=16, blank=True, null=True)
    parts_qty = DjangoModel.IntegerField(blank=True, null=True)
    supplier = DjangoModel.CharField(max_length=16, blank=True, null=True)
    remarks = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    base = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_order_detail'


class TblProductAttr(BaseModel):
    product_id = DjangoModel.IntegerField(blank=True, null=True)
    attribute_group = DjangoModel.CharField(max_length=16, blank=True, null=True)
    attribute_code = DjangoModel.CharField(max_length=8, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_product_attr'


class TblProductPrice(BaseModel):
    product_id = DjangoModel.IntegerField(blank=True, null=True)
    application_start_date = DjangoModel.DateField(blank=True, null=True)
    application_end_date = DjangoModel.DateField(blank=True, null=True)
    product_tax_excluded_price = DjangoModel.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    ccy_excluding_tax = DjangoModel.CharField(max_length=16, blank=True, null=True)
    product_tax_rate = DjangoModel.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    product_tax_in = DjangoModel.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    ccy_including_tax = DjangoModel.CharField(max_length=16, blank=True, null=True)
    product_discount_price = DjangoModel.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    product_discount_currency = DjangoModel.CharField(max_length=16, blank=True, null=True)
    product_price_change = DjangoModel.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    product_currency = DjangoModel.CharField(max_length=16, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_product_price'


class TblStoreSiteInfo(BaseModel):
    store_id = DjangoModel.IntegerField(blank=True, null=True)
    ip_address = DjangoModel.CharField(max_length=64, blank=True, null=True)
    port_no = DjangoModel.CharField(max_length=8, blank=True, null=True)
    db_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    db_host = DjangoModel.CharField(max_length=128, blank=True, null=True)
    db_port_no = DjangoModel.CharField(max_length=8, blank=True, null=True)
    db_user = DjangoModel.CharField(max_length=16, blank=True, null=True)
    db_password = DjangoModel.CharField(max_length=32, blank=True, null=True)
    client_ip = DjangoModel.CharField(max_length=64, blank=True, null=True)
    client_port_no = DjangoModel.CharField(max_length=8, blank=True, null=True)
    server_ip = DjangoModel.CharField(max_length=64, blank=True, null=True)
    server_port_no = DjangoModel.CharField(max_length=8, blank=True, null=True)
    websocket_ip = DjangoModel.CharField(max_length=64, blank=True, null=True)
    websocket_port_no = DjangoModel.CharField(max_length=8, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_store_site_info'


class TblWarehousing(BaseModel):
    order_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    receipt_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    receipt_date = DjangoModel.DateField(blank=True, null=True)
    supplier = DjangoModel.CharField(max_length=16, blank=True, null=True)
    remarks = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    base = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_warehousing'


class TblWarehousingDetail(BaseModel):
    receipt_id = DjangoModel.IntegerField(blank=True, null=True)
    part_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    parts_type = DjangoModel.CharField(max_length=8, blank=True, null=True)
    part_unit = DjangoModel.IntegerField(blank=True, null=True)
    parts_unit_price_tax_inc = DjangoModel.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    parts_currency = DjangoModel.CharField(max_length=16, blank=True, null=True)
    parts_tax_rate = DjangoModel.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    parts_receipt_qty = DjangoModel.IntegerField(blank=True, null=True)
    receipt_status_confirmation = DjangoModel.CharField(max_length=32, blank=True, null=True)
    receipt_parts_checker = DjangoModel.CharField(max_length=32, blank=True, null=True)
    remarks = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    base = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_warehousing_detail'

class TblSupplie(BaseModel):
    sup_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    sup_tel = DjangoModel.CharField(max_length=20, blank=True, null=True)
    sup_addr = DjangoModel.CharField(max_length=64, blank=True, null=True)
    contact_name = DjangoModel.CharField(max_length=20, blank=True, null=True)

    extend = JSONField()
    create_time = DjangoModel.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'tbl_supplie'