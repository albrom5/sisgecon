from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.base.models import BaseModel
from apps.processos.models import ProcessoCompra
from apps.contratos.models import RevisaoContratoCompra
from apps.empresa.models import Pessoa, Funcionario
from apps.produtos.models import Produto


class Pesquisa(BaseModel):
    processo = models.ForeignKey(ProcessoCompra, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    contrato = models.ForeignKey(RevisaoContratoCompra,
                                 on_delete=models.SET_NULL, null=True,
                                 blank=True)
    responsavel = models.ForeignKey(Funcionario, on_delete=models.SET_NULL,
                                    null=True, blank=True)
    prorrogacao_contrato = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class ItemPesquisa(BaseModel):
    pesquisa = models.ForeignKey(Pesquisa, on_delete=models.CASCADE)
    ord_item = models.CharField(verbose_name='Item', max_length=4, null=True,
                                blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=19, decimal_places=6,
                                     validators=[
                                         MinValueValidator(
                                             Decimal('0.000000'))], null=True,
                                     blank=True)
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

    def __str__(self):
        return f'{self.pesquisa} - {self.produto}'


class Proposta(BaseModel):
    pesquisa = models.ForeignKey(Pesquisa, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Pessoa, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    data_recebimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.pesquisa} - {self.fornecedor}'


class ItemProposta(BaseModel):
    proposta = models.ForeignKey(Proposta, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemPesquisa, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=19, decimal_places=6,
                                     validators=[
                                         MinValueValidator(
                                             Decimal('0.000000'))], null=True,
                                     blank=True)
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

    def __str__(self):
        return f'{self.proposta} - {self.item.produto}'
