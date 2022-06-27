# Generated by Django 4.0.4 on 2022-06-27 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_customer_saved_pick_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='card_balance',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='order_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='purchase_percent',
            field=models.FloatField(default=1.0, null=True),
        ),
    ]
