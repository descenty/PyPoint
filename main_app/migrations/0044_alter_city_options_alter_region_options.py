# Generated by Django 4.0.6 on 2022-08-03 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0043_alter_pickpoint_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'Регион', 'verbose_name_plural': 'Регионы'},
        ),
    ]
