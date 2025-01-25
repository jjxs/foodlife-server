app starting...
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class MstAuthority(models.Model):
    permission_type = models.CharField(max_length=20, blank=True, null=True)
    authority_name = models.CharField(max_length=50, blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)
    organization_id = models.IntegerField(blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_authority'


class MstBase(models.Model):
    base_code = models.CharField(max_length=8, blank=True, null=True)
    base_name = models.CharField(max_length=32, blank=True, null=True)
    country = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    address_1 = models.CharField(max_length=128, blank=True, null=True)
    address_2 = models.CharField(max_length=128, blank=True, null=True)
    postal_code = models.CharField(max_length=16, blank=True, null=True)
    contact_id = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    fax_number = models.CharField(max_length=32, blank=True, null=True)
    mail = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_base'


class MstCodeGroup(models.Model):
    name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    extend = models.CharField(max_length=1024, blank=True, null=True)
    option = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'mst_code_group'


class MstCodeValue(models.Model):
    group_id = models.IntegerField()
    code = models.IntegerField()
    name = models.CharField(max_length=500)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=1024, blank=True, null=True)
    extend = models.CharField(max_length=1024, blank=True, null=True)
    option = models.TextField(blank=True, null=True)  # This field type is a guess.
    theme_id = models.CharField(max_length=50, blank=True, null=True)
    menu_count = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_code_value'


class MstCompany(models.Model):
    company_code = models.CharField(max_length=8, blank=True, null=True)
    base_id = models.IntegerField(blank=True, null=True)
    company_name = models.CharField(max_length=64, blank=True, null=True)
    company_name_kana = models.CharField(max_length=256, blank=True, null=True)
    capital = models.CharField(max_length=32, blank=True, null=True)
    representative_id = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    fax_number = models.CharField(max_length=32, blank=True, null=True)
    mail = models.CharField(max_length=256, blank=True, null=True)
    industry = models.CharField(max_length=512, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_company'


class MstCustomer(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    address_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_customer'


class MstEmployee(models.Model):
    emp_number = models.CharField(max_length=16, blank=True, null=True)
    company_id = models.IntegerField(blank=True, null=True)
    org_id = models.IntegerField(blank=True, null=True)
    concurrent_organization_id = models.IntegerField(blank=True, null=True)
    job_code = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    emp_name = models.CharField(max_length=64, blank=True, null=True)
    employment_status = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_employee'


class MstEmployeeInfo(models.Model):
    emp_id = models.IntegerField(blank=True, null=True)
    last_name_kanji = models.CharField(max_length=32, blank=True, null=True)
    last_name_kana = models.CharField(max_length=32, blank=True, null=True)
    first_name_kanji = models.CharField(max_length=32, blank=True, null=True)
    first_name_kana = models.CharField(max_length=32, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    postal_code = models.CharField(max_length=16, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    employment_class = models.IntegerField(blank=True, null=True)
    retirement_date = models.DateField(blank=True, null=True)
    photo = models.CharField(max_length=32, blank=True, null=True)
    phone_number_extension = models.CharField(max_length=32, blank=True, null=True)
    phone_number_personal = models.CharField(max_length=32, blank=True, null=True)
    mail = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_employee_info'


class MstIngredients(models.Model):
    ing_no = models.CharField(max_length=16, blank=True, null=True)
    ing_name = models.CharField(max_length=64, blank=True, null=True)
    ing_cat_id = models.IntegerField(blank=True, null=True)
    stock_unit = models.CharField(max_length=8, blank=True, null=True)
    consumption_unit = models.CharField(max_length=8, blank=True, null=True)
    unit_conv_rate = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    ave_price = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    store_id = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

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
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_ingredients_cat'


class MstMenu(models.Model):
    menu_code = models.CharField(max_length=20, blank=True, null=True)
    menu_name = models.CharField(max_length=50, blank=True, null=True)
    language_code = models.CharField(max_length=10, blank=True, null=True)
    upper_menu_code = models.CharField(max_length=20, blank=True, null=True)
    menu_path = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_menu'


class MstMenuAuthorityRelation(models.Model):
    menu_id = models.IntegerField(primary_key=True)
    authority_id = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_menu_authority_relation'
        unique_together = (('menu_id', 'authority_id'),)


class MstMenuLanguage(models.Model):
    menu_language_code = models.CharField(primary_key=True, max_length=10)
    language = models.CharField(max_length=50)
    menu_name = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_menu_language'
        unique_together = (('menu_language_code', 'language'),)


class MstMessage(models.Model):
    id = models.CharField(max_length=10)
    language = models.CharField(max_length=1024)
    message = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_message'


class MstOrganization(models.Model):
    company_id = models.IntegerField(blank=True, null=True)
    base_id = models.IntegerField(blank=True, null=True)
    org_code = models.CharField(max_length=8, blank=True, null=True)
    org_name = models.CharField(max_length=32, blank=True, null=True)
    upper_organization_id = models.IntegerField(blank=True, null=True)
    org_hierarchy_path = models.CharField(max_length=256, blank=True, null=True)
    org_chief_id = models.IntegerField(blank=True, null=True)
    contact_id = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    fax_number = models.CharField(max_length=32, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_organization'


class MstParameter(models.Model):
    attendance_time = models.TimeField(blank=True, null=True)
    leaving_time = models.TimeField(blank=True, null=True)
    go_directly_time = models.TimeField(blank=True, null=True)
    return_directly_time = models.TimeField(blank=True, null=True)
    break_time_1 = models.TimeField(blank=True, null=True)
    break_return_time_1 = models.TimeField(blank=True, null=True)
    break_time_2 = models.TimeField(blank=True, null=True)
    break_return_time_2 = models.TimeField(blank=True, null=True)
    break_time_3 = models.TimeField(blank=True, null=True)
    break_return_time_3 = models.TimeField(blank=True, null=True)
    break_time_4 = models.TimeField(blank=True, null=True)
    break_return_time_4 = models.TimeField(blank=True, null=True)
    flex_flag = models.BooleanField(blank=True, null=True)
    scheduled_direct_flag = models.BooleanField(blank=True, null=True)
    scheduled_break_flag = models.BooleanField(blank=True, null=True)
    authority_id = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_parameter'


class MstParts(models.Model):
    part_code = models.CharField(max_length=8, blank=True, null=True)
    part_name = models.CharField(max_length=32, blank=True, null=True)
    parts_type = models.CharField(max_length=8, blank=True, null=True)
    part_unit = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_parts'


class MstProduct(models.Model):
    product_code = models.CharField(max_length=16, blank=True, null=True)
    product_name = models.CharField(max_length=32, blank=True, null=True)
    product_unit = models.IntegerField(blank=True, null=True)
    product_unit_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    product_unit_price_currency = models.CharField(max_length=16, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_product'


class MstProductAttr(models.Model):
    product_type = models.CharField(max_length=16, blank=True, null=True)
    attribute_group = models.CharField(max_length=16, blank=True, null=True)
    attribute_code = models.CharField(max_length=8, blank=True, null=True)
    attribute_name = models.CharField(max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_product_attr'


class MstRole(models.Model):
    roll_code = models.CharField(max_length=20, blank=True, null=True)
    role_name = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_role'


class MstStock(models.Model):
    receipt_number = models.CharField(max_length=32, blank=True, null=True)
    part_id = models.IntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=32, blank=True, null=True)
    product_unit = models.IntegerField(blank=True, null=True)
    parts_processing_category = models.CharField(max_length=8, blank=True, null=True)
    part_processing_category_id = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)
    parts_theory_inventory_qty = models.IntegerField(blank=True, null=True)
    parts_inventory_qty = models.IntegerField(blank=True, null=True)
    base = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_stock'


class MstStore(models.Model):
    store_code = models.CharField(max_length=32, blank=True, null=True)
    store_name = models.CharField(max_length=64, blank=True, null=True)
    store_org_id = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    postal_code = models.CharField(max_length=16, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    street_address = models.CharField(max_length=64, blank=True, null=True)
    building_name = models.CharField(max_length=64, blank=True, null=True)
    opening_time = models.CharField(max_length=128, blank=True, null=True)
    remarks = models.CharField(max_length=512, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_store'


class MstUser(models.Model):
    user_account = models.CharField(max_length=30, blank=True, null=True)
    user_name = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    password_last_update_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_user'


class MstUserRoleRelation(models.Model):
    user_id = models.IntegerField(primary_key=True)
    role_id = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_user_role_relation'
        unique_together = (('user_id', 'role_id'),)


class MstUserType(models.Model):
    user_type_id = models.IntegerField(primary_key=True)
    user_type_name = models.CharField(max_length=20, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_user_type'


class MstUserTypeRelation(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_type_id = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=100, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mst_user_type_relation'
        unique_together = (('user_id', 'user_type_id'),)


class TblAttRecord(models.Model):
    working_day = models.DateField(blank=True, null=True)
    attendance_time = models.DateTimeField(blank=True, null=True)
    leaving_time = models.DateTimeField(blank=True, null=True)
    working_time = models.CharField(max_length=8, blank=True, null=True)
    break_time = models.CharField(max_length=8, blank=True, null=True)
    late_time = models.CharField(max_length=8, blank=True, null=True)
    leave_early_time = models.CharField(max_length=8, blank=True, null=True)
    midnight_working_hours = models.CharField(max_length=8, blank=True, null=True)
    holiday_working_hours = models.CharField(max_length=8, blank=True, null=True)
    attendance_category = models.IntegerField(blank=True, null=True)
    emp_id = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_att_record'


class TblAttendance(models.Model):
    working_day = models.DateField(blank=True, null=True)
    time_division = models.IntegerField(blank=True, null=True)
    punch_time = models.DateTimeField(blank=True, null=True)
    emp_id = models.IntegerField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)  # This field type is a guess.
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_attendance'


class TblHolidayDef(models.Model):
    holiday_class = models.CharField(max_length=8, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    authority_id = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_holiday_def'


class TblInspection(models.Model):
    part_id = models.IntegerField(blank=True, null=True)
    part_unit = models.IntegerField(blank=True, null=True)
    parts_unit_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    parts_currency = models.CharField(max_length=16, blank=True, null=True)
    parts_inventory_qty = models.IntegerField(blank=True, null=True)
    inspection_date = models.DateField(blank=True, null=True)
    inspector = models.CharField(max_length=16, blank=True, null=True)
    inspection_result_confirmation = models.CharField(max_length=8, blank=True, null=True)
    remarks = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)
    inspection_delete = models.IntegerField(blank=True, null=True)
    base = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_inspection'


class TblIssue(models.Model):
    goods_issue_number = models.CharField(max_length=32, blank=True, null=True)
    part_id = models.IntegerField(blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    goods_issue_quantity = models.CharField(max_length=16, blank=True, null=True)
    delivery_status_checker = models.CharField(max_length=16, blank=True, null=True)
    goods_issue_indicator = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)
    base = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_issue'


class TblOrder(models.Model):
    order_number = models.CharField(max_length=32, blank=True, null=True)
    orderer = models.CharField(max_length=16, blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    order_address = models.CharField(max_length=128, blank=True, null=True)
    order_phone_number = models.IntegerField(blank=True, null=True)
    order_summary = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)
    base = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_order'


class TblOrderDetail(models.Model):
    ordering_table_unique_id = models.IntegerField(blank=True, null=True)
    part_id = models.IntegerField(blank=True, null=True)
    part_name = models.CharField(max_length=32, blank=True, null=True)
    parts_type = models.CharField(max_length=8, blank=True, null=True)
    parts_unit_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    parts_currency = models.CharField(max_length=16, blank=True, null=True)
    parts_qty = models.IntegerField(blank=True, null=True)
    supplier = models.CharField(max_length=16, blank=True, null=True)
    remarks = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)
    base = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_order_detail'


class TblProductAttr(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    attribute_group = models.CharField(max_length=16, blank=True, null=True)
    attribute_code = models.CharField(max_length=8, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_product_attr'


class TblProductPrice(models.Model):
    product_id = models.IntegerField(blank=True, null=True)
    application_start_date = models.DateField(blank=True, null=True)
    application_end_date = models.DateField(blank=True, null=True)
    product_tax_excluded_price = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    ccy_excluding_tax = models.CharField(max_length=16, blank=True, null=True)
    product_tax_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    product_tax_in = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    ccy_including_tax = models.CharField(max_length=16, blank=True, null=True)
    product_discount_price = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    product_discount_currency = models.CharField(max_length=16, blank=True, null=True)
    product_price_change = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    product_currency = models.CharField(max_length=16, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_product_price'


class TblStoreSiteInfo(models.Model):
    store_id = models.IntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=64, blank=True, null=True)
    port_no = models.CharField(max_length=8, blank=True, null=True)
    db_name = models.CharField(max_length=32, blank=True, null=True)
    db_host = models.CharField(max_length=128, blank=True, null=True)
    db_port_no = models.CharField(max_length=8, blank=True, null=True)
    db_user = models.CharField(max_length=16, blank=True, null=True)
    db_password = models.CharField(max_length=32, blank=True, null=True)
    client_ip = models.CharField(max_length=64, blank=True, null=True)
    client_port_no = models.CharField(max_length=8, blank=True, null=True)
    server_ip = models.CharField(max_length=64, blank=True, null=True)
    server_port_no = models.CharField(max_length=8, blank=True, null=True)
    websocket_ip = models.CharField(max_length=64, blank=True, null=True)
    websocket_port_no = models.CharField(max_length=8, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_store_site_info'


class TblWarehousing(models.Model):
    order_number = models.CharField(max_length=32, blank=True, null=True)
    receipt_number = models.CharField(max_length=32, blank=True, null=True)
    receipt_date = models.DateField(blank=True, null=True)
    supplier = models.CharField(max_length=16, blank=True, null=True)
    remarks = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)
    base = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_warehousing'


class TblWarehousingDetail(models.Model):
    receipt_id = models.IntegerField(blank=True, null=True)
    part_name = models.CharField(max_length=32, blank=True, null=True)
    parts_type = models.CharField(max_length=8, blank=True, null=True)
    part_unit = models.IntegerField(blank=True, null=True)
    parts_unit_price_tax_inc = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    parts_currency = models.CharField(max_length=16, blank=True, null=True)
    parts_tax_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    parts_receipt_qty = models.IntegerField(blank=True, null=True)
    receipt_status_confirmation = models.CharField(max_length=32, blank=True, null=True)
    receipt_parts_checker = models.CharField(max_length=32, blank=True, null=True)
    remarks = models.CharField(max_length=256, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    create_user_id = models.IntegerField(blank=True, null=True)
    create_program = models.CharField(max_length=128, blank=True, null=True)
    last_update_date = models.DateTimeField(blank=True, null=True)
    last_update_user_id = models.IntegerField(blank=True, null=True)
    last_update_program = models.CharField(max_length=128, blank=True, null=True)
    base = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_warehousing_detail'

class TakeoutUser(models.Model):
    user_name = models.CharField(max_length=100)
    user_tel = models.CharField(max_length=100)
    user_address = models.CharField(max_length=200)
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