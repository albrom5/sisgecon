from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel, Status
from apps.produtos.models import Produto, SubGrupoProduto
from apps.processos.models import ProcessoCompra
from apps.empresa.models import (
    Departamento, CentroCusto, ContaContabil, Funcionario
)


class SolicitacaoCompra(BaseModel):
    numsc = models.CharField(verbose_name='SC', max_length=6, unique=True)
    data_emissao = models.DateField(verbose_name='Emitida em',
                                    null=True, blank=True)
    prazo = models.DateField(null=True, blank=True)
    data_rec_compras = models.DateField(null=True, blank=True)
    processo = models.ForeignKey(ProcessoCompra, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'ativo': True})
    objeto = models.CharField(max_length=500, null=True, blank=True)
    justificativa = models.TextField(max_length=1000, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=19, decimal_places=6,
                                      null=True, blank=True)
    area = models.ForeignKey(Departamento, verbose_name='Área',
                             null=True, blank=True,
                             on_delete=models.SET_NULL,
                             limit_choices_to={'ativo': True})
    centro_custo = models.ForeignKey(CentroCusto,
                                     verbose_name='Centro de Custo',
                                     null=True, blank=True,
                                     on_delete=models.SET_NULL,
                                     limit_choices_to={'ativo': True})
    conta_contabil = models.ForeignKey(ContaContabil,
                                       verbose_name='Conta Contábil',
                                       null=True, blank=True,
                                       on_delete=models.SET_NULL,
                                       limit_choices_to={'ativo': True})
    contr_evento = models.CharField(max_length=30, null=True, blank=True)
    evento = models.CharField(max_length=30, null=True, blank=True)

    cadtec = models.FileField(null=True, blank=True)
    responsavel = models.ForeignKey(Funcionario, verbose_name='Responsável',
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    limit_choices_to={'ativo': True})
    status = models.ForeignKey(Status, null=True, blank=True,
                               on_delete=models.SET_NULL,
                               limit_choices_to={'ativo': True})

    @property
    def valor_total_sc(self):
        total = self.itens.filter(ativo=True).aggregate(
            Sum('valor_total'))['valor_total__sum']
        return total or 0

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_total_sc
        super(SolicitacaoCompra, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.numsc} - {self.objeto}'

    class Meta:
        verbose_name = "Solicitação de Compras"
        verbose_name_plural = "Solicitações de Compras"
        ordering = ['numsc']

class ItemSC(BaseModel):
    solicitacao = models.ForeignKey(SolicitacaoCompra, null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    limit_choices_to={'ativo': True},
                                    related_name="itens")
    ord_item = models.CharField(verbose_name='Item', max_length=4, null=True,
                                blank=True)
    subgrupo = models.ForeignKey(SubGrupoProduto, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'ativo': True},
                                 related_name="itemsc_subgrupo")
    produto = models.ForeignKey(Produto, null=True, blank=True,
                                on_delete=models.PROTECT,
                                limit_choices_to={'ativo': True},
                                related_name="itemsc_produto")
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

    @property
    def valor_total_item(self):
        tot_item = self.quantidade * self.valor_unit
        return tot_item or 0

    def get_ord_item(self):
        itens = ItemSC.objects.filter(solicitacao=self.solicitacao)
        if not itens:
            ordem = 1
            return str(ordem)
        ultimo = ItemSC.objects.filter(solicitacao=self.solicitacao).last()
        ordem = int(ultimo.ord_item) + 1
        return str(ordem)

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_total_item
        if self.ord_item is None:
            self.ord_item = self.get_ord_item()
        super(ItemSC, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.ord_item} - {self.produto}'

    class Meta:
        verbose_name = "Item da Solicitação de Compras"
        verbose_name_plural = "Itens da Solicitação de Compras"
        ordering = ['solicitacao', 'ord_item']
