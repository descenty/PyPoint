from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from nested_admin.nested import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from . import models


class OrderedGoodStatusAdminInline(NestedTabularInline):
    model = models.OrderedGoodStatus
    readonly_fields = ('status_type', 'created_at')
    can_delete = False
    extra = 0


class OrderedGoodAdminInline(NestedTabularInline):
    model = models.OrderedGood
    readonly_fields = ('good', 'bar_code')
    inlines = (OrderedGoodStatusAdminInline, )
    can_delete = False
    extra = 0


@admin.register(models.Order)
class OrderAdmin(NestedModelAdmin):
    list_display = ('customer', 'total')
    inlines = (OrderedGoodAdminInline, )
    readonly_fields = ('customer', 'total', 'pick_point', 'pick_point_cell', 'delivery_point')


class OrderAdminInline(NestedTabularInline):
    model = models.Order
    inlines = (OrderedGoodAdminInline, )
    readonly_fields = ('total', 'pick_point', 'pick_point_cell', 'delivery_point')
    extra = 0


@admin.register(models.Customer)
class CustomerAdmin(NestedModelAdmin):
    list_display = ('fio', 'phone')
    inlines = (OrderAdminInline, )
    readonly_fields = ('order_count', 'purchase_percent')


@admin.register(models.PickPoint)
class PickPointAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'rating', 'cells_count')
    readonly_fields = ('rating', )


@admin.register(models.Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating')
    readonly_fields = ('rating', )


class GoodAdminInline(admin.TabularInline):
    model = models.Good
    readonly_fields = ('rating', )
    extra = 0


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')
    readonly_fields = ('rating', )
    inlines = (GoodAdminInline, )


class CartGoodAdminInline(admin.TabularInline):
    model = models.CartGood
    extra = 0


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('count', 'total', 'total_with_discount', 'promo_code_name')
    inlines = (CartGoodAdminInline, )


@admin.register(models.PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('value', 'promo_code_type')


@admin.register(models.Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'image_tag')
    readonly_fields = ('image_tag',)
