from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.base.models import BaseModel, Status
from apps.processos.models import ProcessoCompra
from apps.produtos.models import Produto


class Pregao(BaseModel):
    processo = models.ForeignKey(ProcessoCompra, on_delete=models.CASCADE)
    refer_sistema = models.CharField(
        verbose_name='Número de Referência no Sistema', max_length=20,
        null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True,
                               blank=True, limit_choices_to={'tipo': 'LC',
                                                             'ativo': True})
    numero_edital = models.CharField(max_length=20, null=True, blank=True)
    data_disputa = models.DateTimeField(null=True, blank=True)
    valor_arrematado = models.DecimalField(max_digits=19, decimal_places=6,
                                           null=True, blank=True)
    valor_adjudicado = models.DecimalField(max_digits=19, decimal_places=6,
                                           null=True, blank=True)

    def __str__(self):
        return f'{self.numero_edital} - {self.refer_sistema}'

    class Meta:
        verbose_name = 'Pregão'
        verbose_name_plural = 'Pregões'
        ordering = ['data_disputa']


class Lote(BaseModel):
    pregao = models.ForeignKey(Pregao, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=300, null=True, blank=True)
    numero = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.pregao} - Lote {self.numero}'


class ItemLote(BaseModel):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    ord_item = models.PositiveSmallIntegerField(verbose_name='Item',
                                                null=True, blank=True)
    produto = models.ForeignKey(Produto, null=True, blank=True,
                                on_delete=models.PROTECT,
                                limit_choices_to={'ativo': True})
    descricao = models.CharField(verbose_name='Descrição', max_length=500,
                                 null=True, blank=True)
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

    def get_ord_item(self):
        ultimo = ItemLote.objects.filter(
            lote=self.lote).last()
        if not ultimo:
            ordem = 1
            return ordem
        ordem = ultimo.ord_item + 1
        return ordem

    @property
    def valor_total_item(self):
        tot_item = self.quantidade * self.valor_unit
        return tot_item or 0

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_total_item
        if self.ord_item is None:
            self.ord_item = self.get_ord_item()
        super(ItemLote, self).save(*args, **kwargs)
