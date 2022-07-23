# Generated by Django 4.0.6 on 2022-07-23 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0024_alter_vehicle_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehicle',
            options={'verbose_name': 'Транспорт', 'verbose_name_plural': 'Транспорт'},
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='category',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1, verbose_name='Категория'),
        ),
    ]
