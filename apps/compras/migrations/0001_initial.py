# Generated by Django 3.1.11 on 2021-06-06 17:27

import cuser.fields
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
            ],
            options={
                'verbose_name': 'Item da Solicitação de Compras',
                'verbose_name_plural': 'Itens da Solicitação de Compras',
            },
        ),
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
            ],
            options={
                'verbose_name': 'Solicitação de Compras',
                'verbose_name_plural': 'Solicitações de Compras',
            },
        ),
    ]
