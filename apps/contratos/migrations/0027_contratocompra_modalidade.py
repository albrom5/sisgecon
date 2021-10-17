# Generated by Django 3.1.13 on 2021-10-17 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0009_auto_20211011_1831'),
        ('contratos', '0026_auto_20211011_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratocompra',
            name='modalidade',
            field=models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='processos.modalidade'),
        ),
    ]
