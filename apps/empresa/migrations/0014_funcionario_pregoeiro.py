# Generated by Django 3.1.13 on 2021-09-26 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0013_contato'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='pregoeiro',
            field=models.BooleanField(default=False),
        ),
    ]