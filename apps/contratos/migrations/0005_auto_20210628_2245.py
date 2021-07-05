# Generated by Django 3.1.11 on 2021-06-29 01:45

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0004_itemcontratocompra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcontratocompra',
            name='saldo_fin',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.000000'))], verbose_name='Saldo financeiro'),
        ),
    ]