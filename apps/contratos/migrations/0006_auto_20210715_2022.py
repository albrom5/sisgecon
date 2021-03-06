# Generated by Django 3.1.11 on 2021-07-15 23:22

import cuser.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0013_contato'),
        ('base', '0002_auto_20210601_2122'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contratos', '0005_auto_20210628_2245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contratocompra',
            options={'ordering': ['tipo', 'numero']},
        ),
        migrations.RemoveField(
            model_name='contratocompra',
            name='data_fim',
        ),
        migrations.RemoveField(
            model_name='contratocompra',
            name='data_ini',
        ),
        migrations.RemoveField(
            model_name='contratocompra',
            name='fiscal',
        ),
        migrations.RemoveField(
            model_name='contratocompra',
            name='gestor',
        ),
        migrations.RemoveField(
            model_name='contratocompra',
            name='valor_total',
        ),
        migrations.RemoveField(
            model_name='contratocompra',
            name='versao',
        ),
        migrations.RemoveField(
            model_name='itemcontratocompra',
            name='contrato',
        ),
        migrations.AddField(
            model_name='contratocompra',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.status'),
        ),
        migrations.AlterField(
            model_name='contratocompra',
            name='numero',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='RevisaoContratoCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Inclu??do em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('numero', models.CharField(max_length=9)),
                ('ordem', models.CharField(blank=True, max_length=3, null=True)),
                ('motivo', models.CharField(blank=True, max_length=1000, null=True)),
                ('data_assinatura', models.DateField(verbose_name='Data de Assinatura')),
                ('data_ini', models.DateField(blank=True, null=True, verbose_name='In??cio da Vig??ncia')),
                ('data_fim', models.DateField(blank=True, null=True, verbose_name='Fim da Vig??ncia')),
                ('valor_total', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True)),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revisoes', to='contratos.contratocompra')),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_revisaocontratocompra', to=settings.AUTH_USER_MODEL, verbose_name='Inclu??do por:')),
                ('fiscal', models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fiscais', to='empresa.funcionario')),
                ('gestor', models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gestores', to='empresa.funcionario')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_revisaocontratocompra', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'ordering': ['ordem'],
            },
        ),
        migrations.AddField(
            model_name='itemcontratocompra',
            name='revisao',
            field=models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='contratos.revisaocontratocompra'),
        ),
    ]
