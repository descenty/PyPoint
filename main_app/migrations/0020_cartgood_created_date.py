# Generated by Django 4.0.6 on 2022-07-21 01:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0019_cart_promo_code_name_alter_cartgood_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartgood',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
