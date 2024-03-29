# Generated by Django 4.0.6 on 2022-08-03 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0033_pickpoint_latitude_pickpoint_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodCategory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('shard', models.CharField(max_length=100)),
                ('query', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.goodcategory')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
            },
        ),
    ]
