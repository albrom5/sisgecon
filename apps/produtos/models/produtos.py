from django.db import models
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey

from apps.base.models import BaseModel


class ClasseProduto(BaseModel):
    descricao = models.CharField('Descrição', max_length=200)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Classe de Objeto"
        verbose_name_plural = "Classes de Objeto"


class GrupoProduto(BaseModel):
    classe = models.ForeignKey(ClasseProduto, on_delete=models.PROTECT,
                               limit_choices_to={'ativo': True})
    descricao = models.CharField('Descrição', max_length=200)

    def __str__(self):
        return self.descricao

    class Meta:
        ordering = ["descricao"]
        verbose_name = "Grupo de Objeto"
        verbose_name_plural = "Grupos de Objeto"


class SubGrupoProduto(BaseModel):
    classe = models.ForeignKey(ClasseProduto, on_delete=models.PROTECT,
                               limit_choices_to={'ativo': True})
    grupo = ChainedForeignKey(
        GrupoProduto,
        chained_field='classe',
        chained_model_field='classe',
        show_all=False,
        auto_choose=True,
        sort=True, limit_choices_to={'ativo': True})
    descricao = models.CharField('Descrição', max_length=200)

    def __str__(self):
        return f'{self.classe} - {self.grupo} - {self.descricao}'

    class Meta:
        ordering = ["classe", "grupo", "descricao"]
        verbose_name = "Subgrupo de Objeto"
        verbose_name_plural = "Subgrupos de Objeto"


class UnidadeMedida(BaseModel):
    sigla = models.CharField(max_length=2, unique=True)
    descricao = models.CharField('Descrição', max_length=200)

    def __str__(self):
        return f'{self.sigla} - {self.descricao}'

    class Meta:
        ordering = ["descricao"]
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"


class Produto(BaseModel):
    descricao = models.CharField(verbose_name='Nome', max_length=300,
                                 unique=True)
    subgrupo = models.ForeignKey(SubGrupoProduto, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 limit_choices_to={'ativo': True},
                                 related_name="produto_subgrupo")
    unidade = models.ForeignKey(UnidadeMedida, null=True,
                                on_delete=models.SET_NULL,
                                limit_choices_to={'ativo': True})
    sigla = models.CharField(max_length=5, null=True, blank=True, unique=True)
    especifica = models.TextField(verbose_name='Especificações adicionais',
                                  max_length=1000, null=True, blank=True)
    numprotheus = models.CharField(verbose_name='COD Protheus',
                                   max_length=15, null=True, blank=True,
                                   unique=True)
    ultimoprecocompra = models.DecimalField(
        verbose_name='Último Preço de Compra',
        max_digits=19,
        decimal_places=6,
        null=True, blank=True)
    tabela_eventos = models.BooleanField(
        verbose_name='Tabela de eventos?', default=False)

    def __str__(self):
        return self.descricao

    def get_absolute_url(self):
        return reverse('produto_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['id']


class SubProduto(BaseModel):
    ACRESCIMO = 'Acréscimo'
    DESCONTO = 'Desconto'
    TIPO_DE_FATOR_CHOICES = [
        (ACRESCIMO, 'Acréscimo'),
        (DESCONTO, 'Desconto'),
    ]
    produto = models.ForeignKey(Produto, related_name="subproduto_produto",
                                on_delete=models.CASCADE,
                                limit_choices_to={'ativo': True})
    descricao = models.CharField('Descrição', max_length=200)
    fator = models.DecimalField(max_digits=9, decimal_places=6, null=True,
                                blank=True)
    tipofator = models.CharField(
        max_length=9,
        null=True,
        blank=True,
        choices=TIPO_DE_FATOR_CHOICES,
    )

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Subproduto"
        verbose_name_plural = "Subprodutos"
