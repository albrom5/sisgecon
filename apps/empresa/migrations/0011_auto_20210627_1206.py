# Generated by Django 3.1.11 on 2021-06-27 15:06

from django.db import migrations, models
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0010_auto_20210627_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='cep',
            field=localflavor.br.models.BRPostalCodeField(blank=True, max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='ender_compl',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Complemento'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='logradouro',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Endereço'),
        ),
    ]
