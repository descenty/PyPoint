from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('fio', 'phone')
    readonly_fields = ('order_count', 'purchase_percent')


@admin.register(models.PickPoint)
class PickPointAdmin(admin.ModelAdmin):
    list_display = ('address', 'rating', 'cells_count')
    readonly_fields = ('rating', )


@admin.register(models.Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating')
    readonly_fields = ('rating', )


class GoodAdminInline(admin.TabularInline):
    model = models.Good
    readonly_fields = ('rating', )


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')
    readonly_fields = ('rating', )
    inlines = (GoodAdminInline, )


class CartGoodAdminInline(admin.TabularInline):
    model = models.CartGood


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('count', 'total', 'total_with_discount', 'promo_code_name')
    inlines = (CartGoodAdminInline, )


@admin.register(models.PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('value', 'promo_code_type')

