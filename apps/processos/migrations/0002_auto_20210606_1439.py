# Generated by Django 3.1.11 on 2021-06-06 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20210601_2122'),
        ('processos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processocompra',
            name='modalidade',
            field=models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.PROTECT, to='processos.modalidade'),
        ),
        migrations.AlterField(
            model_name='processocompra',
            name='status',
            field=models.ForeignKey(blank=True, limit_choices_to={'ativo': True, 'tipo': 'PC'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.status'),
        ),
    ]
