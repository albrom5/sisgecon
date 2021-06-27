# Generated by Django 3.1.11 on 2021-06-27 14:45

from django.db import migrations, models
import localflavor.br.models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0008_auto_20210627_1103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pessoa',
            options={'ordering': ['nome']},
        ),
        migrations.AddField(
            model_name='pessoa',
            name='bairro',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='cidade',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='ender_compl',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='ender_num',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='estado',
            field=localflavor.br.models.BRStateField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='logradouro',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='pais',
            field=models.CharField(default='Brasil', max_length=100),
        ),
    ]
