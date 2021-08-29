from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel, Status
from apps.contratos.models import RevisaoContratoCompra, ItemContratoCompra
from apps.produtos.models import Produto


class OrdemFornecimento(BaseModel):
    contrato = models.ForeignKey(RevisaoContratoCompra,
                                 on_delete=models.PROTECT,
                                 limit_choices_to={'is_vigente': True})
    numero = models.PositiveIntegerField(null=True, blank=True)
    numero_format_ano = models.CharField(max_length=10, null=True, blank=True)
    data_emissao = models.DateField(verbose_name='Data de emissão',
                                    null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               limit_choices_to={'tipo': 'OF',
                                                 'ativo': True})

    @property
    def valor_total_of(self):
        total = self.itens.filter(ativo=True).aggregate(
            Sum('valor_total'))['valor_total__sum']
        return total or 0

    def get_sequencial(self):
        data = self.data_emissao
        ano = data.year
        of = OrdemFornecimento.objects.filter(
            ativo=True, data_emissao__year=ano).last()
        if of:
            return of.numero + 1
        else:
            return 1

    @property
    def numero_formatado(self):
        data = self.data_emissao
        ano = data.year
        return f'{str(self.numero).zfill(5)}/{str(ano)}'

    def save(self, *args, **kwargs):
        if self.numero is None or self.numero == '':
            self.numero = self.get_sequencial()
        if self.numero_format_ano is None:
            self.numero_format_ano = self.numero_formatado
        self.valor_total = self.valor_total_of
        super(OrdemFornecimento, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero_format_ano}'

    class Meta:
        ordering = ['numero']
        verbose_name = 'Ordem de Fornecimento'


class ItemOF(BaseModel):
    ordem_fornecimento = models.ForeignKey(OrdemFornecimento,
                                           on_delete=models.CASCADE,
                                           limit_choices_to={'ativo': True},
                                           related_name='itens')
    ord_item = models.PositiveSmallIntegerField(verbose_name='Item',
                                                null=True, blank=True)
    produto = models.ForeignKey(
        ItemContratoCompra, on_delete=models.PROTECT,
        null=True, blank=True,
        limit_choices_to={'ativo': True},
        related_name='produtos')
    descricao = models.CharField(verbose_name='Descrição', max_length=500,
                                 null=True, blank=True)
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

    def get_ord_item(self):
        itens = ItemOF.objects.filter(
            ordem_fornecimento=self.ordem_fornecimento)
        if not itens:
            ordem = 1
            return ordem
        ultimo = ItemOF.objects.filter(
            ordem_fornecimento=self.ordem_fornecimento).last()
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
        super(ItemOF, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.ord_item} - {self.produto}'

    class Meta:
        ordering = ['ord_item']
