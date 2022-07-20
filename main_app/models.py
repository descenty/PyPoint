from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomerManager
from main_app.promo_codes import promo_codes


class Cart(models.Model):
    count = models.PositiveSmallIntegerField(default=0, blank=True, verbose_name='Количество товаров')
    total = models.DecimalField(default=0.00, blank=True, max_digits=10, decimal_places=2, verbose_name='Сумма')
    total_with_discount = models.DecimalField(default=0.00, blank=True, max_digits=10, decimal_places=2, verbose_name='Сумма со скидкой')
    promo_code = models.CharField(max_length=30, blank=True, null=True, verbose_name='Промокод')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина {str(self.customer)}'

    def save(self, *args, **kwargs):
        cart_goods = self.cartgood_set.all()
        self.count = sum(x.quantity for x in cart_goods)
        self.total = sum(x.good.price * x.quantity for x in cart_goods)
        self.total_with_discount = self.total
        if PromoCode.objects.filter(value=self.promo_code).exists():
            promo_code = PromoCode.objects.get(value=self.promo_code)
            promo_code_object = [x[1] for x in promo_codes.items() if x[0][0] == promo_code.promo_code_type][0]
            activated, msg = promo_code_object.activate(self)
        super(Cart, self).save(*args, **kwargs)


class Customer(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True, verbose_name='Телефон')
    email = models.EmailField(max_length=100, blank=True, unique=True, null=True, verbose_name='Электронная почта')
    fio = models.CharField(max_length=50, blank=True, null=True, verbose_name='ФИО')
    order_count = models.PositiveSmallIntegerField(default=0, verbose_name='Количество заказов')
    purchase_percent = models.FloatField(default=1, verbose_name='Процент выкупа')
    card_balance = models.DecimalField(default=0.00, blank=True, max_digits=10, decimal_places=2, verbose_name='Баланс')
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
    image = models.ImageField(upload_to='sellers', null=True, blank=True, verbose_name='Изображение')
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
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, verbose_name='Продавец')
    rating = models.FloatField(default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Good, self).save(*args, **kwargs)
        [x.save() for x in self.cartgood_set.all()]


class CartGood(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')

    def save(self, *args, **kwargs):
        super(CartGood, self).save(*args, **kwargs)
        self.cart.save()

    def delete(self, *args, **kwargs):
        super(CartGood, self).delete(*args, **kwargs)
        self.cart.save()

    def __str__(self):
        return f'{self.good.name} - {self.good.price * self.quantity}'


class OrderedGood(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    bar_code = models.CharField(max_length=20, null=True)
    pick_point_customer = models.ForeignKey(PickPointCustomer, on_delete=models.CASCADE)


class PromoCode(models.Model):
    value = models.CharField(max_length=20, primary_key=True, verbose_name='Значение')
    promo_code_type = models.CharField(max_length=50, choices=tuple(promo_codes.keys()), verbose_name='Тип промокода')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


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

