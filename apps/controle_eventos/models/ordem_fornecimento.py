from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel, Status
from apps.contratos.models import (
    RevisaoContratoCompra, ItemContratoCompra, SubItemContratoCompra
)


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
    valor_total = models.DecimalField(max_digits=19, decimal_places=6,
                                      validators=[
                                          MinValueValidator(
                                              Decimal('0.000000'))], null=True,
                                      blank=True)
    inicio_montagem = models.DateTimeField(null=True, blank=True)
    fim_desmontagem = models.DateTimeField(null=True, blank=True)

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

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

    def decompoe_valor(self):
        valor_unit = self.produto.valor_unit
        subitens = SubItemContratoCompra.objects.filter(
            item_id=self.produto.id).order_by('diaria_inicial')
        periodo = (self.fim_desmontagem - self.inicio_montagem).days + 1
        itens_decompostos = DecomposicaoValor.objects.filter(item=self)
        print(f'Período = {periodo} diárias')
        if itens_decompostos:
            itens_decompostos.delete()
        if not subitens:
            DecomposicaoValor.objects.create(
                item=self, valor_corrigido=valor_unit,
                dias=periodo
            )
        else:
            lista_subitens = list()
            for subitem in subitens:
                if subitem.tipofator == 'Desconto':
                    lista_subitens.append(
                        [subitem.diaria_inicial, subitem.fator]
                    )
            DecomposicaoValor.objects.create(
                item=self, valor_corrigido=valor_unit,
                dias=1
            )

            ultimo_desconto = max(lista_subitens)[0]
            if periodo > 1:
                for subitem in lista_subitens:
                    valor_com_desconto = valor_unit * (subitem[1] / 100)
                    if ultimo_desconto == subitem[0]:
                        diarias = periodo - subitem[0]
                        if diarias <= 0:
                            break
                    else:
                        diarias = 1
                    DecomposicaoValor.objects.create(
                        item=self, valor_corrigido=valor_com_desconto,
                        dias=diarias
                    )

    @property
    def total_item(self):
        tot_item = self.decomposicaovalor_set.filter(ativo=True).aggregate(
            Sum('subtotal'))['subtotal__sum']
        return tot_item or 0

    def atualiza_saldo(self):
        contrato = ItemContratoCompra.objects.get(id=self.produto.id)
        saldo_anterior_contrato = contrato.saldo_fin
        saldo_atualizado_contrato = saldo_anterior_contrato
        if not self._state.adding:
            valor_anterior_of = self._loaded_values['valor_total']
            if valor_anterior_of != self.valor_total:
                saldo_anterior_contrato += valor_anterior_of
                saldo_atualizado_contrato = \
                    saldo_anterior_contrato - self.valor_total
        else:
            saldo_atualizado_contrato = \
                saldo_anterior_contrato - self.valor_total
        contrato.saldo_fin = saldo_atualizado_contrato
        contrato.save()

    def save(self, *args, **kwargs):
        if self.ord_item is None:
            self.ord_item = self.get_ord_item()
        self.valor_total = self.total_item
        self.atualiza_saldo()
        super(ItemOF, self).save(*args, **kwargs)
        self.decompoe_valor()

    def __str__(self):
        return f'{self.ord_item} - {self.produto}'

    class Meta:
        ordering = ['ord_item']


class DecomposicaoValor(BaseModel):
    item = models.ForeignKey(ItemOF, on_delete=models.CASCADE)
    valor_corrigido = models.DecimalField(
        verbose_name='Valor corrigido',
        max_digits=19, decimal_places=6,
        validators=[MinValueValidator(Decimal('0.000000'))], null=True,
        blank=True)
    dias = models.PositiveIntegerField(null=True, blank=True)
    subtotal = models.DecimalField(
        verbose_name='Subtotal',
        max_digits=19, decimal_places=6,
        validators=[MinValueValidator(Decimal('0.000000'))], null=True,
        blank=True)

    def subtotal_periodo(self):
        valor_diaria = self.item.quantidade * self.valor_corrigido * self.dias
        return valor_diaria or 0

    def save(self, *args, **kwargs):
        self.subtotal = self.subtotal_periodo()
        super(DecomposicaoValor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.item} - {self.dias}'
