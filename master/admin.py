from django.contrib import admin
from .models.role import *
from .models.counter import *
from .models.guest import *
from .models.master import *
from .models.menu import *
from .models.order import *
from .models.reservation import *
from .models.seat import *

from django.db.models.fields.related import ManyToOneRel
import master.data.cache_data as cache_data
from django.core.cache import cache
##################### 予約 ##################################



class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_no', 'reservation_time', 'name', 'tel', 'phone', 'number']

# Register your models here.
admin.site.register(Reservation, ReservationAdmin)





##################### Order ##################################
class OrderDetailStatusInline(admin.TabularInline):
    extra = 1
    model = OrderDetailStatus


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = [f.name for f in OrderDetail._meta.get_fields() if not isinstance(f, ManyToOneRel)]
    search_fields = tuple(f.name for f in OrderDetail._meta.get_fields() if not isinstance(f, ManyToOneRel))
    # list_filter = [f.name for f in OrderDetail._meta.get_fields() if not isinstance(f, ManyToOneRel)]
    inlines = [OrderDetailStatusInline]


admin.site.register(OrderDetail, OrderDetailAdmin)


class OrderDetailInline(admin.TabularInline):
    extra = 1
    model = OrderDetail


class OrderAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Order._meta.get_fields() if not isinstance(f, ManyToOneRel)]
    inlines = [OrderDetailInline]


admin.site.register(Order, OrderAdmin)

##################### Menu ##################################

# class MenuInline(admin.TabularInline):
#     extra = 1
#     model = Menu


# class MenuCategoryAdmin(admin.ModelAdmin):
#     inlines = [MenuInline]


# admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(MenuCategory)


class MenuAdmin(admin.ModelAdmin):
    list_display = ['no', 'name', 'stock_status', 'usable', 'price']

    # # save_modelで既存のModelAdminを保存する場合、キャッシュをクリアする
    # def save_model(self, request, obj, form, change):
    #     cache.set('role_auth', None)
    #     cache.set('role_user', None)
    #     super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Menu, MenuAdmin)


class MenuFreeDetailInline(admin.TabularInline):
    extra = 1
    model = MenuFreeDetail


class MenuFreeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'menu', 'free_type', 'usable_time']
    inlines = [MenuFreeDetailInline]


admin.site.register(MenuFree, MenuFreeAdmin)
##################### Role ##################################


class RoleDetailInline(admin.TabularInline):
    extra = 1
    model = RoleDetail


class RoleAdmin(admin.ModelAdmin):
    inlines = [RoleDetailInline]
    list_display = ['name', 'note']

    # save_modelで既存のModelAdminを保存する場合、キャッシュをクリアする
    def save_model(self, request, obj, form, change):
        
        #キャッシュクリア
        cache_data.clear_role()

        super().save_model(request, obj, form, change)


admin.site.register(Role, RoleAdmin)


class RoleUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

    # save_modelで既存のModelAdminを保存する場合、キャッシュをクリアする
    def save_model(self, request, obj, form, change):
        #キャッシュクリア
        cache_data.clear_role()
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(RoleUser, RoleUserAdmin)

##################### Guest ##################################


class GuestDeviceInline(admin.TabularInline):
    extra = 1
    model = GuestDevice


class GuestUserInline(admin.TabularInline):
    extra = 1
    model = GuestUser


class GuestAdmin(admin.ModelAdmin):
    inlines = [GuestDeviceInline, GuestUserInline]


admin.site.register(Guest, GuestAdmin)

##################### Data ##################################


class MasterDataInline(admin.TabularInline):
    extra = 1
    model = MasterData


class MasterDataGroupAdmin(admin.ModelAdmin):

    list_display = [f.name for f in MasterDataGroup._meta.get_fields() if not isinstance(f, ManyToOneRel)]

    inlines = [MasterDataInline]

    ordering = ('domain', 'id', )

    def save_model(self, request, obj, form, change):
        #キャッシュクリア
        cache_data.clear_master()
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(MasterDataGroup, MasterDataGroupAdmin)


class DataAdmin(admin.ModelAdmin):
    # ...
    list_display = ('group_ja', 'code_ja', 'name_ja', 'display_name_ja', 'order_ja', 'note_ja')

    def group_ja(self, obj):
        return obj.group
    group_ja.short_description = "データグループ"

    def code_ja(self, obj):
        return obj.code
    code_ja.short_description = "コード"

    def name_ja(self, obj):
        return obj.name
    name_ja.short_description = "名称"

    def display_name_ja(self, obj):
        return obj.display_name
    display_name_ja.short_description = "表示名"

    def order_ja(self, obj):
        return obj.display_order
    order_ja.short_description = "順番"

    def note_ja(self, obj):
        return obj.note
    note_ja.short_description = "備考"

    #inlines = [DataInline]
    def save_model(self, request, obj, form, change):
        #キャッシュクリア
        cache_data.clear_master()
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(MasterData, DataAdmin)

##################### Seat ##################################


class SeatInline(admin.TabularInline):
    extra = 1
    model = Seat


class SeatGroupAdmin(admin.ModelAdmin):
    inlines = [SeatInline]


# Register your models here.
admin.site.register(SeatGroup, SeatGroupAdmin)


# class SeatCategoryInline(admin.TabularInline):
#     model = SeatCategory

#     def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

#         field = super(SeatCategoryInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

#         if db_field.name == 'group':
#             print(db_field.name)

#         if db_field.name == 'data':
#             field.queryset = field.queryset.all()

#         return field


class SeatAdmin(admin.ModelAdmin):
    # ...
    list_display = [f.name for f in Seat._meta.get_fields() if not isinstance(f, ManyToOneRel)]

    # inlines = [SeatCategoryInline]


# Register your models here.
admin.site.register(Seat, SeatAdmin)


class SeatStatusAdmin(admin.ModelAdmin):
    # ...
    list_display = [f.name for f in SeatStatus._meta.get_fields() if not isinstance(f, ManyToOneRel)]


admin.site.register(SeatStatus, SeatStatusAdmin)
#######################################################
