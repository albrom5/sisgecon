from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.base.models import BaseModel, Status
from apps.processos.models import ProcessoCompra
from apps.empresa.models import Pessoa, Departamento, Funcionario
from apps.produtos.models import Produto, SubGrupoProduto


class AtaRP(BaseModel):
    processo = models.ForeignKey(ProcessoCompra, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    numero = models.PositiveSmallIntegerField(null=True, blank=True)
    numero_format_ano = models.CharField(max_length=9, null=True, blank=True)
    fornecedor = models.ForeignKey(Pessoa, on_delete=models.PROTECT,
                                   limit_choices_to={'fornecedor': True})
    status = models.ForeignKey(Status, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               limit_choices_to={'tipo': 'AP', 'ativo': True})
    data_assinatura = models.DateField(verbose_name='Data de Assinatura',
                                       null=True, blank=True)

    @property
    def numero_formatado(self):
        data = self.data_assinatura
        ano = data.year
        return f'{str(self.numero).zfill(4)}/{str(ano)}'

    def get_sequencial(self):
        data = self.data_assinatura
        ano = data.year
        ata = AtaRP.objects.filter(
            ativo=True, data_assinatura__year=ano).last()
        if ata:
            return ata.numero + 1
        else:
            return 1

    def save(self, *args, **kwargs):
        if self.numero is None or self.numero == '':
            self.numero = self.get_sequencial()
        if self.numero_format_ano is None:
            self.numero_format_ano = self.numero_formatado
        super(AtaRP, self).save(*args, **kwargs)

    def __str__(self):
        return f'ARP n° {self.numero_formatado}'

    class Meta:
        verbose_name = 'Ata de Registro de Preços'
        verbose_name_plural = 'Atas de Registro de Preços'
        ordering = ['data_assinatura', 'numero']


class RevisaoAta(BaseModel):
    ata = models.ForeignKey(AtaRP, on_delete=models.CASCADE,
                            related_name='revisoes')
    numero_aditamento = models.PositiveSmallIntegerField(null=True, blank=True)
    nome_simplificado = models.CharField(max_length=100, null=True, blank=True)
    objeto = models.CharField(max_length=500, null=True, blank=True)
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
                               related_name='gestores_da_ata')
    fiscal = models.ForeignKey(Funcionario, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               limit_choices_to={'ativo': True},
                               related_name='fiscais_da_ata')
    is_vigente = models.BooleanField(default=True)
    cod_protheus = models.CharField(max_length=15, null=True, blank=True)
    data_protheus = models.DateField(null=True, blank=True)
    subgrupo = models.ForeignKey(SubGrupoProduto, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    @property
    def valor_total_ata(self):
        total = self.itemata_set.filter(ativo=True).aggregate(
            Sum('valor_total'))['valor_total__sum']
        return total or 0

    @property
    def numero_formatado(self):
        if self.numero_aditamento is not None:
            data = self.data_assinatura
            ano = data.year
            return f'{str(self.numero_aditamento).zfill(4)}/{str(ano)}'

    def get_sequencial(self):
        data = self.data_assinatura
        ano = data.year
        aditamento = RevisaoAta.objects.filter(
            ativo=True, data_assinatura__year=ano).last()
        if aditamento and aditamento.numero_aditamento is not None:
            return aditamento.numero_aditamento + 1
        else:
            return 1

    def get_ordem(self):
        ultima_revisao = RevisaoAta.objects.filter(ata=self.ata).last()
        if not ultima_revisao:
            ordem = 0
            return ordem
        ordem = int(ultima_revisao.ordem) + 1
        return ordem

    def copia_itens(self):
        itens = ItemAta.objects.filter(
            revisao__ata=self.ata.id, revisao__ordem=self.ordem - 1)
        itens_atuais = ItemAta.objects.filter(revisao=self.id)
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
        self.valor_total = self.valor_total_ata
        super(RevisaoAta, self).save(*args, **kwargs)
        if self.ordem > 0:
            self.copia_itens()

    def tornar_atual_vigente(self):
        RevisaoAta.objects.filter(
            ata=self.ata).order_by('ordem').update(is_vigente=False)
        return

    def __str__(self):
        if self.numero_aditamento is None:
            return f'{self.ata.numero_formatado} - ' \
                   f'{self.nome_simplificado}'
        else:
            return f'{self.ata.numero_formatado} - ' \
                   f'{self.nome_simplificado} - Revisão nº {self.ordem}'

    class Meta:
        ordering = ['ata', 'ordem']


class ItemAta(BaseModel):
    revisao = models.ForeignKey(RevisaoAta, null=True, blank=True,
                                on_delete=models.CASCADE,
                                limit_choices_to={'ativo': True})
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
    def get_saldo_fisico(self):
        saldo_fis = self.saldo_fin / self.valor_unit
        return saldo_fis or 0

    @property
    def get_saldo_financeiro(self):
        saldo_fin = self.saldo_fis / self.valor_unit
        return saldo_fin or 0

    def get_ord_item(self):
        ultimo_item = ItemAta.objects.filter(
            revisao=self.revisao).last()
        if not ultimo_item:
            ordem = 1
            return ordem
        ordem = ultimo_item.ord_item + 1
        return ordem

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_total_item
        if self.ord_item is None:
            self.ord_item = self.get_ord_item()
        super(ItemAta, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.revisao.ata.numero_formatado} ' \
               f'Revisão {self.revisao.ordem} - Item {self.ord_item} - ' \
               f'{self.produto}'

    class Meta:
        ordering = ['ord_item']


class SubItemAta(BaseModel):
    TIPO_DE_FATOR_CHOICES = [
        ('ACRS', 'Acréscimo'),
        ('DESC', 'Desconto sobre diária'),
        ('SUPR', 'Desconto sobre equipamento'),

    ]
    item = models.ForeignKey(ItemAta, on_delete=models.CASCADE)
    descricao = models.CharField('Descrição', max_length=200)
    fator = models.DecimalField(max_digits=9, decimal_places=6, null=True,
                                blank=True)
    tipofator = models.CharField(
        max_length=9,
        null=True,
        blank=True,
        choices=TIPO_DE_FATOR_CHOICES,
    )
    diaria_inicial = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.descricao
