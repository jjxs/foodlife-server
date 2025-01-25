
from django.db import models as DjangoModel
from app.db.models.base import BaseModel

# 使わないテーブルstart
class MstOrgUserRelation(BaseModel):

    user_id = DjangoModel.FloatField(blank=True, null=True)
    org_id = DjangoModel.FloatField(blank=True, null=True)
    display_seq = DjangoModel.FloatField(blank=True, null=True)
    effective_start_date = DjangoModel.DateField(blank=True, null=True)
    effective_end_date = DjangoModel.DateField(blank=True, null=True)
    email_send_flag = DjangoModel.CharField(max_length=1, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.FloatField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.FloatField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_org_user_relation'


class MstOrganization(BaseModel):

    org_code = DjangoModel.CharField(max_length=10, blank=True, null=True)
    org_type = DjangoModel.CharField(max_length=10, blank=True, null=True)
    company_id = DjangoModel.FloatField(blank=True, null=True)
    org_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    is_delete = DjangoModel.CharField(max_length=1, blank=True, null=True)
    address1_id = DjangoModel.CharField(max_length=150, blank=True, null=True)
    address2_id = DjangoModel.CharField(max_length=150, blank=True, null=True)
    closing_process_not_covered = DjangoModel.CharField(max_length=1, blank=True, null=True)
    invoice = DjangoModel.CharField(max_length=1, blank=True, null=True)
    sigma_if_flag = DjangoModel.CharField(max_length=1, blank=True, null=True)
    suppliers_code = DjangoModel.CharField(max_length=10, blank=True, null=True)
    note = DjangoModel.CharField(max_length=512, blank=True, null=True)
    scm_org_flag = DjangoModel.CharField(max_length=1, blank=True, null=True)
    parent_org_id = DjangoModel.FloatField(blank=True, null=True)
    org_hierarchy = DjangoModel.CharField(max_length=512, blank=True, null=True)
    summary_org_cd = DjangoModel.CharField(max_length=10, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.FloatField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.FloatField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'mst_organization'


class MstUserHistory(BaseModel):

    user_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    language = DjangoModel.CharField(max_length=3, blank=True, null=True)
    email = DjangoModel.CharField(max_length=100, blank=True, null=True)
    id_delete_date = DjangoModel.DateField(blank=True, null=True)
    entry_appd_date = DjangoModel.DateField(blank=True, null=True)
    one_time_password_issue = DjangoModel.CharField(max_length=1, blank=True, null=True)
    password = DjangoModel.CharField(max_length=500, blank=True, null=True)
    password_last_update_date = DjangoModel.DateField(blank=True, null=True)
    account_lock_times = DjangoModel.IntegerField(blank=True, null=True)
    note = DjangoModel.CharField(max_length=512, blank=True, null=True)
    change_datetime = DjangoModel.DateField()
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.FloatField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.FloatField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_user_history'
        unique_together = (('id', 'change_datetime'),)
# 使わないテーブルend

class MstAuthority(BaseModel):
    permission_type = DjangoModel.CharField(max_length=20, blank=True, null=True)
    authority_name = DjangoModel.CharField(max_length=50, blank=True, null=True)
    role_id = DjangoModel.IntegerField(blank=True, null=True)
    organization_id = DjangoModel.IntegerField(blank=True, null=True)
    company_id = DjangoModel.IntegerField(blank=True, null=True)
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_authority'


class MstBase(BaseModel):
    base_code = DjangoModel.CharField(max_length=8, blank=True, null=True)
    base_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    country = DjangoModel.IntegerField(blank=True, null=True)
    state = DjangoModel.IntegerField(blank=True, null=True)
    address_1 = DjangoModel.CharField(max_length=128, blank=True, null=True)
    address_2 = DjangoModel.CharField(max_length=128, blank=True, null=True)
    postal_code = DjangoModel.CharField(max_length=16, blank=True, null=True)
    contact_id = DjangoModel.IntegerField(blank=True, null=True)
    phone_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    fax_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    mail = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_base'


class MstCodeGroup(BaseModel):
    name = DjangoModel.CharField(max_length=200)
    display_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    domain = DjangoModel.CharField(max_length=100, blank=True, null=True)
    note = DjangoModel.CharField(max_length=200, blank=True, null=True)
    display_order = DjangoModel.IntegerField(blank=True, null=True)
    extend = DjangoModel.CharField(max_length=1024, blank=True, null=True)
    option = DjangoModel.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mst_code_group'


class MstCodeValue(BaseModel):
    group_id = DjangoModel.IntegerField()
    code = DjangoModel.IntegerField()
    name = DjangoModel.CharField(max_length=500)
    display_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    display_order = DjangoModel.IntegerField(blank=True, null=True)
    note = DjangoModel.CharField(max_length=1024, blank=True, null=True)
    extend = DjangoModel.CharField(max_length=1024, blank=True, null=True)
    option = DjangoModel.TextField(blank=True, null=True)  # This field type is a guess.
    theme_id = DjangoModel.CharField(max_length=50, blank=True, null=True)
    menu_count = DjangoModel.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_code_value'


class MstCompany(BaseModel):
    company_code = DjangoModel.CharField(max_length=8, blank=True, null=True)
    base_id = DjangoModel.IntegerField(blank=True, null=True)
    company_name = DjangoModel.CharField(max_length=64, blank=True, null=True)
    company_name_kana = DjangoModel.CharField(max_length=256, blank=True, null=True)
    capital = DjangoModel.CharField(max_length=32, blank=True, null=True)
    representative_id = DjangoModel.IntegerField(blank=True, null=True)
    phone_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    fax_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    mail = DjangoModel.CharField(max_length=256, blank=True, null=True)
    industry = DjangoModel.CharField(max_length=512, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_company'


class MstCustomer(BaseModel):
    user_id = DjangoModel.IntegerField(blank=True, null=True)
    birthday = DjangoModel.DateField(blank=True, null=True)
    age = DjangoModel.IntegerField(blank=True, null=True)
    sex = DjangoModel.CharField(max_length=1, blank=True, null=True)
    address_id = DjangoModel.IntegerField(blank=True, null=True)
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_customer'


class MstEmployee(BaseModel):
    emp_number = DjangoModel.CharField(max_length=16, blank=True, null=True)
    company_id = DjangoModel.IntegerField(blank=True, null=True)
    org_id = DjangoModel.IntegerField(blank=True, null=True)
    concurrent_organization_id = DjangoModel.IntegerField(blank=True, null=True)
    job_code = DjangoModel.IntegerField(blank=True, null=True)
    user_id = DjangoModel.IntegerField(blank=True, null=True)
    emp_name = DjangoModel.CharField(max_length=64, blank=True, null=True)
    employment_status = DjangoModel.IntegerField(blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_employee'


class MstEmployeeInfo(BaseModel):
    emp_id = DjangoModel.IntegerField(blank=True, null=True)
    last_name_kanji = DjangoModel.CharField(max_length=32, blank=True, null=True)
    last_name_kana = DjangoModel.CharField(max_length=32, blank=True, null=True)
    first_name_kanji = DjangoModel.CharField(max_length=32, blank=True, null=True)
    first_name_kana = DjangoModel.CharField(max_length=32, blank=True, null=True)
    birthday = DjangoModel.DateField(blank=True, null=True)
    sex = DjangoModel.IntegerField(blank=True, null=True)
    postal_code = DjangoModel.CharField(max_length=16, blank=True, null=True)
    address = DjangoModel.CharField(max_length=128, blank=True, null=True)
    hire_date = DjangoModel.DateField(blank=True, null=True)
    employment_class = DjangoModel.IntegerField(blank=True, null=True)
    retirement_date = DjangoModel.DateField(blank=True, null=True)
    photo = DjangoModel.CharField(max_length=32, blank=True, null=True)
    phone_number_extension = DjangoModel.CharField(max_length=32, blank=True, null=True)
    phone_number_personal = DjangoModel.CharField(max_length=32, blank=True, null=True)
    mail = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_employee_info'


class MstMenu(BaseModel):
    menu_code = DjangoModel.CharField(max_length=20, blank=True, null=True)
    menu_name = DjangoModel.CharField(max_length=50, blank=True, null=True)
    language_code = DjangoModel.CharField(max_length=10, blank=True, null=True)
    upper_menu_code = DjangoModel.CharField(max_length=20, blank=True, null=True)
    menu_path = DjangoModel.CharField(max_length=100, blank=True, null=True)
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_menu'


class MstMenuAuthorityRelation(BaseModel):
    menu_id = DjangoModel.IntegerField(primary_key=True)
    authority_id = DjangoModel.IntegerField()
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_menu_authority_relation'
        unique_together = (('menu_id', 'authority_id'),)


class MstMenuLanguage(BaseModel):
    menu_language_code = DjangoModel.CharField(primary_key=True, max_length=10)
    language = DjangoModel.CharField(max_length=50)
    menu_name = DjangoModel.CharField(max_length=50, blank=True, null=True)
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_menu_language'
        unique_together = (('menu_language_code', 'language'),)


class MstMessage(BaseModel):
    language = DjangoModel.CharField(max_length=1024)
    message = DjangoModel.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_message'


class MstParameter(BaseModel):
    attendance_time = DjangoModel.TimeField(blank=True, null=True)
    leaving_time = DjangoModel.TimeField(blank=True, null=True)
    go_directly_time = DjangoModel.TimeField(blank=True, null=True)
    return_directly_time = DjangoModel.TimeField(blank=True, null=True)
    break_time_1 = DjangoModel.TimeField(blank=True, null=True)
    break_return_time_1 = DjangoModel.TimeField(blank=True, null=True)
    break_time_2 = DjangoModel.TimeField(blank=True, null=True)
    break_return_time_2 = DjangoModel.TimeField(blank=True, null=True)
    break_time_3 = DjangoModel.TimeField(blank=True, null=True)
    break_return_time_3 = DjangoModel.TimeField(blank=True, null=True)
    break_time_4 = DjangoModel.TimeField(blank=True, null=True)
    break_return_time_4 = DjangoModel.TimeField(blank=True, null=True)
    flex_flag = DjangoModel.BooleanField(blank=True, null=True)
    scheduled_direct_flag = DjangoModel.BooleanField(blank=True, null=True)
    scheduled_break_flag = DjangoModel.BooleanField(blank=True, null=True)
    authority_id = DjangoModel.IntegerField(blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_parameter'


class MstParts(BaseModel):
    part_code = DjangoModel.CharField(max_length=8, blank=True, null=True)
    part_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    parts_type = DjangoModel.CharField(max_length=8, blank=True, null=True)
    part_unit = DjangoModel.IntegerField(blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_parts'


class MstProduct(BaseModel):
    product_code = DjangoModel.CharField(max_length=16, blank=True, null=True)
    product_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    product_unit = DjangoModel.IntegerField(blank=True, null=True)
    product_unit_price = DjangoModel.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    product_unit_price_currency = DjangoModel.CharField(max_length=16, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_product'


class MstProductAttr(BaseModel):
    product_type = DjangoModel.CharField(max_length=16, blank=True, null=True)
    attribute_group = DjangoModel.CharField(max_length=16, blank=True, null=True)
    attribute_code = DjangoModel.CharField(max_length=8, blank=True, null=True)
    attribute_name = DjangoModel.CharField(max_length=128, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_product_attr'


class MstRole(BaseModel):
    roll_code = DjangoModel.CharField(max_length=20, blank=True, null=True)
    role_name = DjangoModel.CharField(max_length=100, blank=True, null=True)
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_role'


class MstStock(BaseModel):
    receipt_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    part_id = DjangoModel.IntegerField(blank=True, null=True)
    part_type = DjangoModel.IntegerField(blank=True, null=True)
    product_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    product_unit = DjangoModel.IntegerField(blank=True, null=True)
    parts_processing_category = DjangoModel.CharField(max_length=8, blank=True, null=True)
    part_processing_category_id = DjangoModel.IntegerField(blank=True, null=True)
    remarks = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    parts_theory_inventory_qty = DjangoModel.IntegerField(blank=True, null=True)
    parts_inventory_qty = DjangoModel.IntegerField(blank=True, null=True)
    parts_inventory_actual = DjangoModel.IntegerField(blank=True, null=True)
    base = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_stock'



class MstStockHistory(BaseModel):
    receipt_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    part_id = DjangoModel.IntegerField(blank=True, null=True)
    part_type = DjangoModel.IntegerField(blank=True, null=True)
    product_name = DjangoModel.CharField(max_length=32, blank=True, null=True)
    product_unit = DjangoModel.IntegerField(blank=True, null=True)
    parts_processing_category = DjangoModel.CharField(max_length=8, blank=True, null=True)
    part_processing_category_id = DjangoModel.IntegerField(blank=True, null=True)
    remarks = DjangoModel.CharField(max_length=256, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    parts_theory_inventory_qty = DjangoModel.IntegerField(blank=True, null=True)
    parts_inventory_qty = DjangoModel.IntegerField(blank=True, null=True)
    base = DjangoModel.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_stock_history'


class MstStore(BaseModel):
    store_code = DjangoModel.CharField(max_length=32, blank=True, null=True)
    store_name = DjangoModel.CharField(max_length=64, blank=True, null=True)
    store_org_id = DjangoModel.IntegerField(blank=True, null=True)
    phone_number = DjangoModel.CharField(max_length=32, blank=True, null=True)
    postal_code = DjangoModel.CharField(max_length=16, blank=True, null=True)
    state = DjangoModel.IntegerField(blank=True, null=True)
    city = DjangoModel.CharField(max_length=32, blank=True, null=True)
    street_address = DjangoModel.CharField(max_length=64, blank=True, null=True)
    building_name = DjangoModel.CharField(max_length=64, blank=True, null=True)
    opening_time = DjangoModel.CharField(max_length=128, blank=True, null=True)
    remarks = DjangoModel.CharField(max_length=512, blank=True, null=True)
    create_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_store'



class MstTimeDivision(BaseModel):
    time_division_code = DjangoModel.CharField(max_length=8, blank=True, null=True)
    time_division_name = DjangoModel.CharField(max_length=16, blank=True, null=True)
    calculation_category = DjangoModel.CharField(max_length=1, blank=True, null=True)
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=128, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_time_division'


class MstUserRoleRelation(BaseModel):
    user_id = DjangoModel.IntegerField(primary_key=True)
    role_id = DjangoModel.IntegerField()
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_user_role_relation'
        unique_together = (('user_id', 'role_id'),)


class MstUserType(BaseModel):
    user_type_id = DjangoModel.IntegerField(primary_key=True)
    user_type_name = DjangoModel.CharField(max_length=20, blank=True, null=True)
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_user_type'


class MstUserTypeRelation(BaseModel):
    user_id = DjangoModel.IntegerField(primary_key=True)
    user_type_id = DjangoModel.IntegerField()
    created_date = DjangoModel.DateTimeField(blank=True, null=True)
    create_user_id = DjangoModel.IntegerField(blank=True, null=True)
    create_program = DjangoModel.CharField(max_length=100, blank=True, null=True)
    last_update_date = DjangoModel.DateTimeField(blank=True, null=True)
    last_update_user_id = DjangoModel.IntegerField(blank=True, null=True)
    last_update_program = DjangoModel.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_user_type_relation'
        unique_together = (('user_id', 'user_type_id'),)

class MstUser2(BaseModel):
    account = DjangoModel.CharField(unique=True, max_length=64)
    password = DjangoModel.CharField(max_length=256,blank=True, null=True)
    level = DjangoModel.IntegerField(blank=True, null=True)
    point = DjangoModel.IntegerField(blank=True, null=True)
    gift_count = DjangoModel.IntegerField(blank=True, null=True)
    user_name = DjangoModel.CharField(max_length=32)
    sex = DjangoModel.IntegerField(blank=True, null=True)
    phone_number = DjangoModel.CharField(max_length=32)
    remarks = DjangoModel.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'mst_user'

