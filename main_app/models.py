from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomerManager


class Customer(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, primary_key=True)
    email = models.EmailField(max_length=100, unique=True)
    fio = models.CharField(max_length=50, null=True)
    order_count = models.IntegerField(null=True)
    purchase_percent = models.FloatField(null=True)
    card_balance = models.PositiveIntegerField(null=True)
    saved_pick_points = models.ManyToManyField('PickPoint')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomerManager()


class PickPoint(models.Model):
    address = models.CharField(max_length=50)
    rating = models.FloatField(default=4.95)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cells_count = models.IntegerField(default=0)


class PickPointCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pick_point = models.ForeignKey(PickPoint, on_delete=models.CASCADE)
    cell = models.IntegerField(null=True)


class Seller(models.Model):
    name = models.CharField(max_length=30)


class Good(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='images', null=True)
    price = models.IntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)


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

