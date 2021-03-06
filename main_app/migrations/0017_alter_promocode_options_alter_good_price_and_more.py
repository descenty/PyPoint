# Generated by Django 4.0.6 on 2022-07-20 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_cart_total_with_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promocode',
            options={'verbose_name': 'Промокод', 'verbose_name_plural': 'Промокоды'},
        ),
        migrations.AlterField(
            model_name='good',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='promo_code_type',
            field=models.CharField(choices=[('DISCOUNT_5', 'Скидка 5%'), ('DISCOUNT_10', 'Скидка 10%'), ('DISCOUNT_20', 'Скидка 20%')], max_length=50, verbose_name='Тип промокода'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='value',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='sellers', verbose_name='Изображение'),
        ),
    ]
