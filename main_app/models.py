from django.db import models


class Customer(models.Model):
    fio = models.CharField()
    phone = models.IntegerField()
    order_count = models.IntegerField()
    purchase_percent = models.FloatField()
    card_balance = models.IntegerField()
    saved_pick_points = models.ManyToManyField('PickPoint')


class Good(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    image = models.ImageField(upload_to='images')
    bar_code = models.IntegerField()
    price = models.IntegerField()


class OrderedGood(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    customer = models.ForeignKey('PickPointCustomer', on_delete=models.CASCADE)


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


class PickPoint(models.Model):
    address = models.CharField(max_length=50)
    rating = models.FloatField()
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cells_count = models.IntegerField()
    max_goods = models.IntegerField()
    goods = models.ForeignKey(OrderedGood, on_delete=models.CASCADE)


class PickPointCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pick_point = models.ForeignKey(PickPoint, on_delete=models.CASCADE)
    cell = models.IntegerField()
