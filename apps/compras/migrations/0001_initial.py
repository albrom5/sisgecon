# Generated by Django 3.1.11 on 2021-06-02 00:19

import cuser.fields
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('processos', '0001_initial'),
        ('produtos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacaoCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('numsc', models.CharField(max_length=6, unique=True, verbose_name='SC')),
                ('data_emissao', models.DateField(blank=True, null=True)),
                ('prazo', models.DateField(blank=True, null=True)),
                ('data_rec_compras', models.DateField(blank=True, null=True)),
                ('objeto', models.CharField(blank=True, max_length=250, null=True)),
                ('justificativa', models.TextField(blank=True, max_length=1000, null=True)),
                ('valor_total', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True)),
                ('centro_custo', models.CharField(blank=True, max_length=30, null=True)),
                ('conta_contabil', models.CharField(blank=True, max_length=30, null=True)),
                ('contr_evento', models.CharField(blank=True, max_length=30, null=True)),
                ('evento', models.CharField(blank=True, max_length=30, null=True)),
                ('cadtec', models.FileField(blank=True, null=True, upload_to='')),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_solicitacaocompra', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('processo', models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='processos.processo')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_solicitacaocompra', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'verbose_name': 'Solicitação de Compras',
                'verbose_name_plural': 'Solicitações de Compras',
            },
        ),
        migrations.CreateModel(
            name='ItemSC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('ord_item', models.CharField(blank=True, max_length=4, null=True)),
                ('descricao', models.CharField(blank=True, max_length=200, null=True)),
                ('quantidade', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.000000'))])),
                ('diaria', models.IntegerField(blank=True, null=True)),
                ('valor_unit', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.000000'))])),
                ('valor_total', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.000000'))])),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_itemsc', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('produto', models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='itemsc_produto', to='produtos.produto')),
                ('solicitacao', models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itemsc_sc', to='compras.solicitacaocompra')),
                ('subgrupo', models.ForeignKey(blank=True, limit_choices_to={'ativo': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='itemsc_subgrupo', to='produtos.subgrupoproduto')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_itemsc', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'verbose_name': 'Item da Solicitação de Compras',
                'verbose_name_plural': 'Itens da Solicitação de Compras',
            },
        ),
    ]