import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel, Status
from apps.contratos.models import (
    RevisaoContratoCompra, ItemContratoCompra, SubItemContratoCompra
)
from .eventos import Evento, SubEvento


class OrdemFornecimento(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL,
                               null=True, blank=True)
    subevento = models.ForeignKey(SubEvento, on_delete=models.SET_NULL,
                                  null=True, blank=True)
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
    quantidade_anterior = models.DecimalField(max_digits=19, decimal_places=6,
                                              validators=[MinValueValidator(
                                                 Decimal('0.000000'))],
                                              null=True, blank=True)
    # Campo diária deste model não é usado para cálculo de valor, apenas para
    # mostrar o total de diárias o item.
    diaria = models.IntegerField(null=True, blank=True)
    valor_total = models.DecimalField(max_digits=19, decimal_places=6,
                                      validators=[
                                          MinValueValidator(
                                              Decimal('0.000000'))], null=True,
                                      blank=True)
    valor_total_anterior = models.DecimalField(max_digits=19, decimal_places=6,
                                               validators=[MinValueValidator(
                                                   Decimal('0.000000'))],
                                               null=True, blank=True)
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
        subitens_contrato = SubItemContratoCompra.objects.filter(
            item_id=self.produto.id).order_by('diaria_inicial')
        data_final_corrigida = \
            self.fim_desmontagem - datetime.timedelta(seconds=1)
        periodo = (data_final_corrigida - self.inicio_montagem).days + 1
        itens_decompostos = DecomposicaoValor.objects.filter(item=self)
        print(f'Período = {periodo} diárias')
        if itens_decompostos:
            itens_decompostos.delete()
        if not subitens_contrato:
            DecomposicaoValor.objects.create(
                item=self, valor_corrigido=valor_unit,
                dias=periodo, desconto=100
            )
        else:
            lista_subitens = list()
            subitens_of = SubItemOF.objects.filter(item_of=self)
            diferenca = 0
            if subitens_of:
                for sub in subitens_of:
                    if sub.item_contrato.tipofator == 'SUPR':
                        sub.item_contrato.fator *= -1
                    diferenca += valor_unit * (sub.item_contrato.fator / 100)
            valor_unit += diferenca
            for subitem in subitens_contrato:
                if subitem.tipofator == 'DESC':
                    lista_subitens.append(
                        [subitem.diaria_inicial, subitem.fator]
                    )
            DecomposicaoValor.objects.create(
                item=self, valor_corrigido=valor_unit,
                dias=1, desconto=100
            )
            ultimo_desconto = max(lista_subitens)[0]
            if periodo > 1:
                for subitem in lista_subitens:
                    valor_com_desconto = valor_unit * (subitem[1] / 100)
                    if ultimo_desconto == subitem[0]:
                        diarias = periodo - subitem[0]
                        if diarias < 0:
                            break
                        else:
                            diarias += 1
                    else:
                        diarias = 1
                    DecomposicaoValor.objects.create(
                        item=self, valor_corrigido=valor_com_desconto,
                        dias=diarias, desconto=subitem[1]
                    )

    @property
    def total_item(self):
        tot_item = self.decomposicaovalor_set.filter(ativo=True).aggregate(
            Sum('subtotal'))['subtotal__sum']
        return tot_item or 0

    @property
    def total_diaria(self):
        tot_diaria = self.decomposicaovalor_set.filter(ativo=True).aggregate(
            Sum('dias'))['dias__sum']
        return tot_diaria or 0

    def armazena_valores_anteriores(self):
        self.quantidade_anterior = self.quantidade
        self.valor_total_anterior = self.total_item

    def atualiza_saldo(self):
        item_contrato = ItemContratoCompra.objects.get(id=self.produto.id)
        if item_contrato.revisao.contrato.controle_de_saldo == 'FIN':
            saldo_anterior_contrato = item_contrato.saldo_fin
            saldo_atualizado_contrato = saldo_anterior_contrato
            if self._state.adding:
                saldo_atualizado_contrato = \
                    saldo_anterior_contrato - self.total_item
            else:
                valor_anterior_of = self.valor_total_anterior
                if valor_anterior_of != self.total_item:
                    saldo_anterior_contrato += valor_anterior_of
                    saldo_atualizado_contrato = \
                        saldo_anterior_contrato - self.total_item
            item_contrato.saldo_fin = saldo_atualizado_contrato
        else:
            saldo_anterior_contrato = item_contrato.saldo_fis
            saldo_atualizado_contrato = saldo_anterior_contrato
            if self._state.adding:
                saldo_atualizado_contrato = \
                    saldo_anterior_contrato - self.total_diaria
            else:
                quantidade_anterior_of = self.quantidade_anterior
                if quantidade_anterior_of != self.total_diaria:
                    saldo_anterior_contrato += quantidade_anterior_of
                    saldo_atualizado_contrato = \
                        saldo_anterior_contrato - self.total_diaria
            item_contrato.saldo_fis = saldo_atualizado_contrato
        item_contrato.save()

    def atualiza_valor_total(self):
        total = self.total_item
        ItemOF.objects.filter(id=self.id).update(valor_total=total)

    def delete(self, *args, **kwargs):
        item_contrato = ItemContratoCompra.objects.get(id=self.produto.id)
        if item_contrato.revisao.contrato.controle_de_saldo == 'FIN':
            saldo_anterior_contrato = item_contrato.saldo_fin
            saldo_atualizado_contrato = \
                saldo_anterior_contrato + self.total_item
            item_contrato.saldo_fin = saldo_atualizado_contrato
        else:
            saldo_anterior_contrato = item_contrato.saldo_fis
            saldo_atualizado_contrato = \
                saldo_anterior_contrato + self.quantidade
            item_contrato.saldo_fis = saldo_atualizado_contrato
        item_contrato.save()
        super(ItemOF, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.ord_item is None:
            self.ord_item = self.get_ord_item()
        self.armazena_valores_anteriores()
        super(ItemOF, self).save(*args, **kwargs)
        self.decompoe_valor()
        self.atualiza_saldo()
        self.atualiza_valor_total()

    def __str__(self):
        return f'{self.ord_item} - {self.produto}'

    class Meta:
        ordering = ['ord_item']


class SubItemOF(BaseModel):
    item_of = models.ForeignKey(ItemOF, on_delete=models.CASCADE)
    item_contrato = models.ForeignKey(SubItemContratoCompra,
                                      on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.item_contrato}'


class DecomposicaoValor(BaseModel):
    item = models.ForeignKey(ItemOF, on_delete=models.CASCADE)
    desconto = models.DecimalField(max_digits=9, decimal_places=6, null=True,
                                   blank=True)
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
        return f'{self.item} - {self.dias} - {self.desconto}%'
