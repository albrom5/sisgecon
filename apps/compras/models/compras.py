from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel
from apps.produtos.models import Produto, SubGrupoProduto
from apps.processos.models import ProcessoCompra


class SolicitacaoCompra(BaseModel):
    numsc = models.CharField(verbose_name='SC', max_length=6, unique=True)
    data_emissao = models.DateField(null=True, blank=True)
    prazo = models.DateField(null=True, blank=True)
    data_rec_compras = models.DateField(null=True, blank=True)
    processo = models.ForeignKey(ProcessoCompra, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'ativo': True})
    objeto = models.CharField(max_length=500, null=True, blank=True)
    justificativa = models.TextField(max_length=1000, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=19, decimal_places=6,
                                      null=True, blank=True)

    centro_custo = models.CharField(max_length=30, null=True, blank=True)
    conta_contabil = models.CharField(max_length=30, null=True, blank=True)
    contr_evento = models.CharField(max_length=30, null=True, blank=True)
    evento = models.CharField(max_length=30, null=True, blank=True)

    cadtec = models.FileField(null=True, blank=True)

# TODO Criar campos status, responsável, área (com relacionamentos)

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


class ItemSC(BaseModel):
    solicitacao = models.ForeignKey(SolicitacaoCompra, null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    limit_choices_to={'ativo': True},
                                    related_name="itens")
    ord_item = models.CharField(max_length=4, null=True, blank=True)
    subgrupo = models.ForeignKey(SubGrupoProduto, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'ativo': True},
                                 related_name="itemsc_subgrupo")
    produto = models.ForeignKey(Produto, null=True, blank=True,
                                on_delete=models.PROTECT,
                                limit_choices_to={'ativo': True},
                                related_name="itemsc_produto")
    descricao = models.CharField(max_length=500, null=True, blank=True)
    quantidade = models.DecimalField(max_digits=19, decimal_places=6,
                                     validators=[
                                         MinValueValidator(
                                             Decimal('0.000000'))], null=True,
                                     blank=True)
    diaria = models.IntegerField(null=True, blank=True)
    valor_unit = models.DecimalField(max_digits=19, decimal_places=6,
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

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_total_item
        super(ItemSC, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.ord_item} - {self.produto}'

    class Meta:
        verbose_name = "Item da Solicitação de Compras"
        verbose_name_plural = "Itens da Solicitação de Compras"
