# Generated by Django 4.0.6 on 2022-07-17 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_cart_remove_customer_basket_cartgood_customer_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cart',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.cart'),
        ),
    ]
