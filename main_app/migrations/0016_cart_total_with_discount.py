# Generated by Django 4.0.6 on 2022-07-20 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_promocode_alter_cart_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_with_discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, verbose_name='Сумма со скидкой'),
        ),
    ]
