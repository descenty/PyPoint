# Generated by Django 4.0.6 on 2022-08-03 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0037_alter_goodcategory_query'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodcategory',
            name='query',
            field=models.CharField(max_length=2000),
        ),
    ]
