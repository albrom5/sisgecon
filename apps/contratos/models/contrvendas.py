from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.base.models import BaseModel
from apps.empresa.models import Pessoa
from apps.produtos.models import Produto


class ContratoVenda(BaseModel):
    numero = models.PositiveSmallIntegerField(null=True, blank=True)
    data_assinaatura = models.DateField(null=True, blank=True)


class RevisaoContratoVenda(BaseModel):
    contrato = models.ForeignKey(ContratoVenda, on_delete=models.CASCADE,
                                 related_name='revisoes')
    cliente = models.ForeignKey(Pessoa, on_delete=models.PROTECT,
                                limit_choices_to={'cliente': True})
    is_vigente = models.BooleanField(default=True)


class ItemContratoVenda(BaseModel):
    revisao = models.ForeignKey(RevisaoContratoVenda, on_delete=models.CASCADE)
    ordem = models.PositiveSmallIntegerField(null=True, blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=500, null=True, blank=True)
    quantidade = models.DecimalField(max_digits=19, decimal_places=6,
                                     validators=[
                                         MinValueValidator(
                                             Decimal('0.000000'))], null=True,
                                     blank=True)
    diaria = models.IntegerField(null=True, blank=True)
    valor_unit = models.DecimalField(verbose_name='Valor unitário',
                                     max_digits=19, decimal_places=6,
                                     validators=[
                                         MinValueValidator(
                                             Decimal('0.000000'))], null=True,
                                     blank=True)
    valor_total = models.DecimalField(max_digits=19, decimal_places=6,
                                      validators=[
                                          MinValueValidator(
                                              Decimal('0.000000'))], null=True,
                                      blank=True)
    saldo_fis = models.DecimalField(verbose_name='Saldo Físico',
                                    max_digits=19, decimal_places=6,
                                    validators=[
                                        MinValueValidator(
                                            Decimal('0.000000'))], null=True,
                                    blank=True)
    saldo_fin = models.DecimalField(verbose_name='Saldo financeiro',
                                    max_digits=19, decimal_places=6,
                                    validators=[
                                        MinValueValidator(
                                            Decimal('0.000000'))], null=True,
                                    blank=True)
