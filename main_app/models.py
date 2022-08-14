from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.safestring import mark_safe
from django.utils.timezone import now

from .managers import CustomerManager
from main_app.promo_codes import promo_codes


class Cart(models.Model):
    count = models.PositiveSmallIntegerField('Количество товаров', default=0, blank=True)
    total = models.DecimalField('Сумма', default=0.00, blank=True, max_digits=10, decimal_places=2)
    total_with_discount = models.DecimalField('Сумма со скидкой', default=0.00, blank=True, max_digits=10,
                                              decimal_places=2)
    promo_code = models.CharField('Промокод', max_length=30, blank=True, null=True)
    promo_code_name = models.CharField('Название промокода', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина {str(self.customer)}'

    def save(self, *args, **kwargs):
        cart_goods = self.cart_goods.all()
        self.count = cart_goods.count()
        self.total = sum(x.good.price * x.quantity for x in cart_goods if x.selected)
        self.total_with_discount = self.total

        activated = False
        if PromoCode.objects.filter(value=self.promo_code).exists():
            promo_code = PromoCode.objects.get(value=self.promo_code)
            promo_code_items = [x for x in promo_codes.items() if x[0][0] == promo_code.promo_code_type][0]
            self.promo_code_name = promo_code_items[0][1]
            promo_code_object = promo_code_items[1]
            activated, msg = promo_code_object.activate(self)
        elif not activated:
            self.promo_code = None
            self.promo_code_name = None
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
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Корзина')
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomerManager()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Region(models.Model):
    name = models.CharField(max_length=75)

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class City(models.Model):
    name = models.CharField(max_length=75)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class PickPoint(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='pick_points', verbose_name='Город')
    address = models.CharField('Адрес', max_length=100)
    rating = models.FloatField('Рейтинг', default=4.95)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name='pick_points', verbose_name='Владелец')
    cells_count = models.PositiveSmallIntegerField('Количество ячеек', default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

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
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина', related_name='cart_goods')
    created_date = models.DateTimeField(default=now, editable=False)
    selected = models.BooleanField('Выбран', blank=True, default=True)

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.delete(*args, **kwargs)
        else:
            super(CartGood, self).save(*args, **kwargs)
        self.cart.save()

    def delete(self, *args, **kwargs):
        super(CartGood, self).delete(*args, **kwargs)
        self.cart.save()

    def __str__(self):
        return f'{self.good.name} - {self.good.price * self.quantity}'


class Order(models.Model):
    class OrderStatusType(models.TextChoices):
        CREATED = 'Создан'
        IN_WORK = 'В работе'
        COMPLETED = 'Завершен'

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент')
    total = models.DecimalField(default=0.00, blank=True, max_digits=10, decimal_places=2, verbose_name='Сумма')
    pick_point = models.ForeignKey(PickPoint, null=True, blank=True, on_delete=models.CASCADE,
                                   verbose_name='Пункт выдачи')
    pick_point_cell = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Ячейка')
    delivery_point = models.CharField(max_length=150, null=True, blank=True, verbose_name='Адрес доставки')
    status_type = models.CharField('Статус', choices=OrderStatusType.choices, max_length=30, default=OrderStatusType.CREATED)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'


class OrderedGood(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='Товар')
    bar_code = models.CharField('ШК', max_length=10, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='ordered_goods')

    def __str__(self):
        return f'{self.bar_code} {self.good.name}'

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'


class Driver(models.Model):
    fio = models.CharField('ФИО', max_length=50)
    phone = models.CharField('Телефон', max_length=11, unique=True)
    passport = models.CharField('Паспортные данные', max_length=100)
    license = models.CharField('Водительские права', max_length=50)
    payroll_card = models.CharField('Номер зарплатной карты', max_length=16, blank=True, null=True)
    fuel_card = models.CharField('Номер топливной карты', max_length=16, blank=True, null=True)
    hourly_rate = models.PositiveSmallIntegerField('Почасовая ставка', blank=True, null=True)


class Vehicle(models.Model):
    vehicle_types = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    name = models.CharField('Наименование', max_length=30)
    license_plate = models.CharField('Регистрационный номер', max_length=8)
    category = models.CharField('Категория', choices=vehicle_types, max_length=1)
    # registration = models.ImageField('Свидетельство о регистрации', upload_to='vehicle/registrations')
    # insurance = models.ImageField('ОСАГО И КАСКО', upload_to='vehicles/insurances', null=True, blank=True)
    photo = models.ImageField('Фотография', upload_to='vehicles/photos', null=True, blank=True)
    ready_for_carriage = models.BooleanField('Готова к перевозкам')
    in_work = models.BooleanField('В работе')

    def image_tag(self):
        return mark_safe(f'<img src="{self.photo.url}" width="150"/>')

    image_tag.short_description = 'Фотография'
    image_tag.allow_tags = True

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорт'


class Delivery(models.Model):
    sender_address = models.CharField('Адрес отправителя', max_length=100)
    recipient_address = models.CharField('Адрес получателя', max_length=100)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    driver_payment = models.PositiveSmallIntegerField('Оплата')
    ordered_goods = models.ManyToManyField(OrderedGood)


class DeliveryStatus(models.Model):
    class DeliveryStatusType(models.TextChoices):
        CREATED = 'Создана'
        FORMED = 'Сформирована'
        TRANSIT = 'В пути'
        COMPLETED = 'Завершена'
        CANCELED = 'Отменена'

    status_type = models.CharField('Статус', choices=DeliveryStatusType.choices, max_length=30)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='statuses')


class PromoCode(models.Model):
    value = models.CharField(max_length=20, primary_key=True, verbose_name='Значение')
    promo_code_type = models.CharField(max_length=50, choices=tuple(promo_codes.keys()), verbose_name='Тип промокода')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class OrderedGoodStatus(models.Model):
    class OrderedGoodStatusType(models.TextChoices):
        CREATED = 'Создан'
        FORMED = 'Сформирован'
        SENT = 'Отправлен'
        ARRIVED = 'Прибыл в пункт выдачи'
        RECEIVED = 'Получен клиентом'
        CANCELED = 'Отменён'

    status_type = models.CharField('Статус', choices=OrderedGoodStatusType.choices, max_length=30)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    ordered_good = models.ForeignKey(OrderedGood, on_delete=models.CASCADE, related_name='statuses')

    class Meta:
        verbose_name = 'Статус товара'
        verbose_name_plural = 'Статусы товара'


class GoodCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    url = models.CharField(max_length=200)
    shard = models.CharField(max_length=200)
    query = models.CharField(max_length=2000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class MessageRoom(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='own_message_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(Customer, related_name='message_rooms')


class Message(models.Model):
    room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)