# Generated by Django 3.1.11 on 2021-06-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0009_auto_20210627_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='ender_compl',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='COmplemento'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='ender_num',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='logradouro',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Rua, Avenida, etc...'),
        ),
    ]