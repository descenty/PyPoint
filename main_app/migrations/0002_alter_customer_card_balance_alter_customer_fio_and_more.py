# Generated by Django 4.0.6 on 2022-07-09 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='card_balance',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='fio',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='order_count',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='purchase_percent',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='saved_pick_points',
            field=models.ManyToManyField(blank=True, to='main_app.pickpoint'),
        ),
    ]
