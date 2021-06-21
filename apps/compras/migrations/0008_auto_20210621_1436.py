# Generated by Django 3.1.11 on 2021-06-21 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0004_centrocusto_contacontabil'),
        ('base', '0002_auto_20210601_2122'),
        ('compras', '0007_solicitacaocompra_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacaocompra',
            name='responsavel',
            field=models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresa.funcionario'),
        ),
        migrations.AddField(
            model_name='solicitacaocompra',
            name='status',
            field=models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.status'),
        ),
        migrations.AlterField(
            model_name='solicitacaocompra',
            name='centro_custo',
            field=models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresa.centrocusto'),
        ),
        migrations.AlterField(
            model_name='solicitacaocompra',
            name='conta_contabil',
            field=models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='empresa.contacontabil'),
        ),
    ]
