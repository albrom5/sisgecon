# Generated by Django 3.1.13 on 2021-08-15 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0015_remove_contratocompra_data_entrega_notificacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='revisaocontratocompra',
            name='cod_protheus',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='revisaocontratocompra',
            name='data_protheus',
            field=models.DateField(blank=True, null=True),
        ),
    ]
