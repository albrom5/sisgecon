from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel
from apps.produtos.models import Produto
from apps.empresa.models import Departamento, Funcionario, Pessoa
from apps.processos.models import ProcessoCompra


class ContratoCompra(BaseModel):
    TIPO_CONTRATO = [
        ('CCO', 'Substitutivo Contratual'),
        ('CCN', 'Termo Contratual')
    ]
    SUBTIPO = [
        ('AS', 'Autorização de Serviço'),
        ('OC', 'Ordem de Compra')
    ]
    processo = models.ForeignKey(ProcessoCompra, on_delete=models.PROTECT,
                                 null=True, blank=True,
                                 limit_choices_to={'ativo': True})
    tipo = models.CharField(max_length=3, choices=TIPO_CONTRATO)
    subtipo = models.CharField(max_length=2, choices=SUBTIPO, null=True,
                               blank=True)
    numero = models.CharField(max_length=9, null=True, blank=True)
    fornecedor = models.ForeignKey(Pessoa, on_delete=models.PROTECT,
                                   limit_choices_to={'fornecedor': True})
    versao = models.CharField(max_length=3, null=True, blank=True)
    objeto = models.CharField(max_length=500)
    data_assinatura = models.DateField(verbose_name='Data de Assinatura')
    data_ini = models.DateField(verbose_name='Início da Vigência', null=True,
                                blank=True)
    data_fim = models.DateField(verbose_name='Fim da Vigência', null=True,
                                blank=True)
    valor_total = models.DecimalField(max_digits=19, decimal_places=6,
                                      null=True, blank=True)
    area = models.ForeignKey(Departamento, on_delete=models.SET_NULL,
                             null=True, blank=True,
                             limit_choices_to={'ativo': True})
    gestor = models.ForeignKey(Funcionario, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               limit_choices_to={'ativo': True},
                               related_name='gestores')
    fiscal = models.ForeignKey(Funcionario, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               limit_choices_to={'ativo': True},
                               related_name='fiscais')

    @property
    def valor_total_contrato(self):
        total = self.itens.filter(ativo=True).aggregate(
            Sum('valor_total'))['valor_total__sum']
        return total or 0

    def get_sequencial(self):
        tipo = self.tipo
        data = self.data_assinatura
        ano = data.year
        contrato = ContratoCompra.objects.filter(
            ativo=True, tipo=tipo, data_assinatura__year=ano).last()
        if contrato:
            ultimo_numero = contrato.numero
            ultimo_numero = ultimo_numero.split('/')
            ultimo_numero = int(ultimo_numero[0])
            numero = ultimo_numero + 1
            return f'{str(numero).zfill(4)}/{str(ano)}'
        else:
            return f'0001/{str(ano)}'

    def save(self, *args, **kwargs):
        if self.numero is None:
            self.numero = self.get_sequencial()
        self.valor_total = self.valor_total_contrato
        super(ContratoCompra, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero} - {self.objeto}'

    class Meta:
        ordering = ['tipo', 'data_assinatura', 'numero']


class ItemContratoCompra(BaseModel):
    contrato = models.ForeignKey(ContratoCompra, null=True, blank=True,
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'ativo': True},
                                 related_name="itens")
    ord_item = models.CharField(verbose_name='Item', max_length=4, null=True,
                                blank=True)
    produto = models.ForeignKey(Produto, null=True, blank=True,
                                on_delete=models.PROTECT,
                                limit_choices_to={'ativo': True},
                                related_name="produtos")
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
    saldo_fis = models.DecimalField(max_digits=19, decimal_places=6,
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

    @property
    def valor_total_item(self):
        tot_item = self.quantidade * self.valor_unit
        return tot_item or 0

    def get_ord_item(self):
        itens = ItemContratoCompra.objects.filter(contrato=self.contrato)
        if not itens:
            ordem = 1
            return str(ordem)
        ultimo = ItemContratoCompra.objects.filter(
            contrato=self.contrato).last()
        ordem = int(ultimo.ord_item) + 1
        return str(ordem)

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_total_item
        if self.ord_item is None:
            self.ord_item = self.get_ord_item()
        super(ItemContratoCompra, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.ord_item} - {self.produto}'

    class Meta:
        ordering = ['ord_item']
