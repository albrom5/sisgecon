# Generated by Django 3.1.11 on 2021-06-27 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0011_auto_20210627_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='cep',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='CEP'),
        ),
    ]