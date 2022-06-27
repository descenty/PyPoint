# Generated by Django 4.0.4 on 2022-06-27 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_customer_card_balance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='saved_pick_points',
        ),
        migrations.AlterField(
            model_name='customer',
            name='card_balance',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='order_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='purchase_percent',
            field=models.FloatField(null=True),
        ),
    ]
