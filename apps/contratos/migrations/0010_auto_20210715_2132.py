# Generated by Django 3.1.11 on 2021-07-16 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0009_auto_20210715_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisaocontratocompra',
            name='ordem',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
