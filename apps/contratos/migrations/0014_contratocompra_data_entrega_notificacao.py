# Generated by Django 3.1.11 on 2021-08-09 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0013_auto_20210727_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratocompra',
            name='data_entrega_notificacao',
            field=models.DateField(blank=True, null=True),
        ),
    ]