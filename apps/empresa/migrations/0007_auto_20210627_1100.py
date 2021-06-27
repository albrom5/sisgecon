# Generated by Django 3.1.11 on 2021-06-27 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0006_auto_20210622_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='tipo',
            field=models.CharField(blank=True, choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, null=True),
        ),
    ]
