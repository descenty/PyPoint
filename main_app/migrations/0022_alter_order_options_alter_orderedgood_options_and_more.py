# Generated by Django 4.0.6 on 2022-07-22 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0021_delivery_driver_vehicle_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderedgood',
            options={'verbose_name': 'Заказанный товар', 'verbose_name_plural': 'Заказанные товары'},
        ),
        migrations.AddField(
            model_name='cartgood',
            name='selected',
            field=models.BooleanField(blank=True, default=True, verbose_name='Выбран'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pick_point',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.pickpoint', verbose_name='Пункт выдачи'),
        ),
        migrations.AlterField(
            model_name='orderedgood',
            name='bar_code',
            field=models.CharField(max_length=10, null=True, verbose_name='ШК'),
        ),
        migrations.AlterField(
            model_name='orderedgood',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.good', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='orderedgood',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_goods', to='main_app.order'),
        ),
    ]
