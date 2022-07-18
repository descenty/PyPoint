from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomerManager


class Cart(models.Model):
    count = models.PositiveSmallIntegerField(default=0, verbose_name='Количество товаров')
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Сумма')
    promo_code = models.CharField(max_length=30, null=True, verbose_name='Промокод')


class Customer(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True, verbose_name='Телефон')
    email = models.EmailField(max_length=100, blank=True, unique=True, null=True, verbose_name='Электронная почта')
    fio = models.CharField(max_length=50, blank=True, null=True, verbose_name='ФИО')
    order_count = models.PositiveSmallIntegerField(default=0, verbose_name='Количество заказов')
    purchase_percent = models.FloatField(default=1, verbose_name='Процент выкупа')
    card_balance = models.PositiveIntegerField(default=0, verbose_name='Баланс')
    saved_pick_points = models.ManyToManyField('PickPoint', blank=True, verbose_name='Сохраненные пункты выдачи')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, blank=True, null=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomerManager()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class PickPoint(models.Model):
    address = models.CharField(max_length=50)
    rating = models.FloatField(default=4.95)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cells_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Пункт выдачи'
        verbose_name_plural = 'Пункты выдачи'

    def __str__(self):
        return self.address


class PickPointCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pick_point = models.ForeignKey(PickPoint, on_delete=models.CASCADE)
    cell = models.PositiveSmallIntegerField(null=True)


class Seller(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='sellers', null=True, verbose_name='Изображение')
    rating = models.FloatField(default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return self.name


class Good(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(max_length=500, verbose_name='Описание')
    image = models.ImageField(upload_to='goods', null=True, verbose_name='Изображение')
    price = models.PositiveIntegerField(verbose_name='Цена')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, verbose_name='Продавец')
    rating = models.FloatField(default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class CartGood(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')


class OrderedGood(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    bar_code = models.CharField(max_length=20, null=True)
    pick_point_customer = models.ForeignKey(PickPointCustomer, on_delete=models.CASCADE)


class GoodsStatus(models.Model):
    class StatusType(models.TextChoices):
        CREATED = 0
        FORMED = 1
        SENT = 2
        ARRIVED = 3
        RECEIVED = 4
        CANCELED = 5
        SENT_BACK = 6
    type = models.IntegerField(choices=StatusType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    good = models.ForeignKey(OrderedGood, on_delete=models.CASCADE)

