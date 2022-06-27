# Generated by Django 4.0.4 on 2022-06-27 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_customer_options_alter_customer_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='fio',
        ),
        migrations.AlterField(
            model_name='customer',
            name='card_balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='order_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='purchase_percent',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='saved_pick_points',
            field=models.ManyToManyField(null=True, to='main_app.pickpoint'),
        ),
    ]
