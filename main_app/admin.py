from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('fio', 'phone')


@admin.register(models.PickPoint)
class PickPointAdmin(admin.ModelAdmin):
    list_display = ('address', 'rating', 'cells_count')


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')


@admin.register(models.Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'price')


class CartGoodAdminInline(admin.TabularInline):
    model = models.CartGood


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('count', 'total')
    inlines = [CartGoodAdminInline, ]

    # def cart_goods(self, cart: models.Cart):
    #     return cart.cartgood_set.all()

