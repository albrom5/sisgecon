# Generated by Django 3.1.11 on 2021-06-20 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0003_auto_20210618_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='tabela_eventos',
            field=models.BooleanField(default=False, verbose_name='Tabela de eventos?'),
        ),
    ]
