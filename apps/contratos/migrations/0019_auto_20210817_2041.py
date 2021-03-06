# Generated by Django 3.1.13 on 2021-08-17 23:41

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0018_auto_20210815_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcontratocompra',
            name='saldo_fis',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.000000'))], verbose_name='Saldo Físico'),
        ),
    ]
