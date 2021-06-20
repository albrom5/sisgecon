# Generated by Django 3.1.11 on 2021-06-18 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0002_auto_20210616_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.CharField(max_length=300, unique=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='especifica',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Especificações adicionais'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='numprotheus',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='COD Protheus'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='tabela_eventos',
            field=models.BooleanField(default=False, verbose_name='Pertence à tabela de eventos'),
        ),
    ]
