# Generated by Django 4.0.4 on 2022-06-28 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_alter_customer_card_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pickpoint',
            name='max_goods',
        ),
        migrations.AlterField(
            model_name='pickpoint',
            name='cells_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pickpoint',
            name='rating',
            field=models.FloatField(default=4.95),
        ),
    ]
