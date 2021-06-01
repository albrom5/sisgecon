from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel, Processo
from apps.produtos.models import Produto, SubGrupoProduto


class ProcessoCompra(BaseModel):
    processo = models.OneToOneField(Processo, on_delete=models.PROTECT)
    objeto = models.CharField(max_length=250, null=True, blank=True)
# TODO Criar campos tipo de processo, status, responsável, área (com relacionamentos)

    def __str__(self):
        return self.processo.numero_sei


class SolicitacaoCompra(BaseModel):
    numsc = models.CharField(verbose_name='SC', max_length=6, unique=True)
    data_emissao = models.DateField(null=True, blank=True)
    prazo = models.DateField(null=True, blank=True)
    data_rec_compras = models.DateField(null=True, blank=True)
    processo = models.ForeignKey(ProcessoCompra, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'ativo': True})
    objeto = models.CharField(max_length=250, null=True, blank=True)
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
        total = self.itemsc_sc.filter(ativo=True).aggregate(
            Sum('valor_total'))['total__sc']
        return total or 0

    def __str__(self):
        return f'{self.numsc} - {self.objeto}'

    class Meta:
        verbose_name = "Solicitação de Compras"
        verbose_name_plural = "Solicitações de Compras"


class ItemSC(BaseModel):
    solicitacao = models.ForeignKey(SolicitacaoCompra, null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    limit_choices_to={'ativo': True},
                                    related_name="itemsc_sc")
    ord_item = models.CharField(max_length=4, null=True, blank=True)
    subgrupo = models.ForeignKey(SubGrupoProduto, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'ativo': True},
                                 related_name="itemsc_subgrupo")
    produto = models.ForeignKey(Produto, null=True, blank=True,
                                on_delete=models.PROTECT,
                                limit_choices_to={'ativo': True},
                                related_name="itemsc_produto")
    descricao = models.CharField(max_length=200, null=True, blank=True)
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

    def __str__(self):
        return f'{self.ord_item} - {self.produto}'

    class Meta:
        verbose_name = "Item da Solicitação de Compras"
        verbose_name_plural = "Itens da Solicitação de Compras"
