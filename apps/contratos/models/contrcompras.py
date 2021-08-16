from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel, Status
from apps.empresa.models import Departamento, Funcionario, Pessoa
from apps.processos.models import ProcessoCompra
from apps.produtos.models import Produto


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
    numero = models.PositiveSmallIntegerField(null=True, blank=True)
    numero_format_ano = models.CharField(max_length=9, null=True, blank=True)
    fornecedor = models.ForeignKey(Pessoa, on_delete=models.PROTECT,
                                   limit_choices_to={'fornecedor': True})
    status = models.ForeignKey(Status, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               limit_choices_to={'tipo': 'CC', 'ativo': True})
    data_assinatura = models.DateField(verbose_name='Data de Assinatura',
                                       null=True, blank=True)

    @property
    def numero_formatado(self):
        data = self.data_assinatura
        ano = data.year
        return f'{str(self.numero).zfill(4)}/{str(ano)}'

    @property
    def numero_formatado_com_tipo(self):
        return f'{self.tipo} {self.numero_formatado}'

    def get_sequencial(self):
        tipo = self.tipo
        data = self.data_assinatura
        ano = data.year
        contrato = ContratoCompra.objects.filter(
            ativo=True, tipo=tipo, data_assinatura__year=ano).last()
        if contrato:
            return contrato.numero + 1
        else:
            return 1

    def save(self, *args, **kwargs):
        if self.numero is None or self.numero == '':
            self.numero = self.get_sequencial()
        if self.numero_format_ano is None:
            self.numero_format_ano = self.numero_formatado
        super(ContratoCompra, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero_formatado_com_tipo}'

    class Meta:
        verbose_name = 'Contrato de Compras'
        verbose_name_plural = 'Contratos de Compras'
        ordering = ['tipo', 'data_assinatura', 'numero']


class RevisaoContratoCompra(BaseModel):
    contrato = models.ForeignKey(ContratoCompra, on_delete=models.CASCADE,
                                 related_name='revisoes')
    numero_aditamento = models.PositiveSmallIntegerField(null=True, blank=True)
    objeto = models.CharField(max_length=500)
    ordem = models.PositiveSmallIntegerField(null=True, blank=True)
    motivo = models.CharField(max_length=1000, null=True, blank=True)
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
    is_vigente = models.BooleanField(default=True)
    cod_protheus = models.CharField(max_length=15, null=True, blank=True)
    data_protheus = models.DateField(null=True, blank=True)

    @property
    def valor_total_contrato(self):
        total = self.itens.filter(ativo=True).aggregate(
            Sum('valor_total'))['valor_total__sum']
        return total or 0

    @property
    def numero_formatado(self):
        if self.numero_aditamento is not None:
            data = self.data_assinatura
            ano = data.year
            return f'{str(self.numero_aditamento).zfill(4)}/{str(ano)}'

    @property
    def numero_formatado_com_tipo(self):
        if self.numero_aditamento is not None:
            return f'{self.contrato.tipo} {self.numero_formatado}'

    def get_sequencial(self):
        tipo = self.contrato.tipo
        data = self.data_assinatura
        ano = data.year
        aditamento = RevisaoContratoCompra.objects.filter(
            ativo=True, contrato__tipo=tipo, data_assinatura__year=ano).last()
        if aditamento and aditamento.numero_aditamento is not None:
            return aditamento.numero_aditamento + 1
        else:
            return 1

    def get_ordem(self):
        aditamentos = RevisaoContratoCompra.objects.filter(
            contrato=self.contrato
        )
        if not aditamentos:
            ordem = 0
            return ordem
        ultimo = RevisaoContratoCompra.objects.filter(
            contrato=self.contrato).last()
        ordem = int(ultimo.ordem) + 1
        return ordem

    def copia_itens(self):
        itens = ItemContratoCompra.objects.filter(revisao__contrato=self.contrato.id, revisao__ordem=self.ordem - 1)
        itens_atuais = ItemContratoCompra.objects.filter(revisao=self.id)
        if len(itens_atuais) == 0:
            for item in itens:
                item.pk = None
                item.revisao = self
                item.save()

    def save(self, *args, **kwargs):
        if self.ordem is None:
            self.ordem = self.get_ordem()
        if self.numero_aditamento is None and self.ordem != 0:
            self.numero_aditamento = self.get_sequencial()
        self.tornar_atual_vigente()
        self.valor_total = self.valor_total_contrato
        super(RevisaoContratoCompra, self).save(*args, **kwargs)
        if self.ordem > 0:
            self.copia_itens()

    def tornar_atual_vigente(self):
        RevisaoContratoCompra.objects.filter(
            contrato=self.contrato).order_by('ordem').update(is_vigente=False)
        return

    def __str__(self):
        if self.numero_aditamento is None:
            return f'{self.contrato.numero_formatado_com_tipo} - {self.objeto}'
        else:
            return f'Aditamento {self.numero_formatado_com_tipo} - {self.ordem}º da Contratação ' \
                   f'{self.contrato.numero_formatado_com_tipo}'

    class Meta:
        ordering = ['contrato', 'ordem']


class ItemContratoCompra(BaseModel):
    revisao = models.ForeignKey(RevisaoContratoCompra, null=True, blank=True,
                                on_delete=models.CASCADE,
                                limit_choices_to={'ativo': True},
                                related_name="itens")
    ord_item = models.PositiveSmallIntegerField(verbose_name='Item',
                                                null=True, blank=True)
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

    @property
    def valor_total_item(self):
        tot_item = self.quantidade * self.valor_unit
        return tot_item or 0

    @property
    def saldo_financeiro(self):
        saldo_fin = self.saldo_fis * self.valor_unit
        return saldo_fin or 0

    def get_ord_item(self):
        itens = ItemContratoCompra.objects.filter(revisao=self.revisao)
        if not itens:
            ordem = 1
            return ordem
        ultimo = ItemContratoCompra.objects.filter(
            revisao=self.revisao).last()
        ordem = ultimo.ord_item + 1
        return ordem

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_total_item
        if self.ord_item is None:
            self.ord_item = self.get_ord_item()
        if self.saldo_fis is None:
            self.saldo_fis = self.quantidade
        super(ItemContratoCompra, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.ord_item} - {self.produto}'

    class Meta:
        ordering = ['ord_item']
