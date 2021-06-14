from django.contrib import admin

from .models import (
    ClasseProduto,
    GrupoProduto,
    SubGrupoProduto,
    UnidadeMedida,
    Produto,
    SubProduto
)


@admin.register(ClasseProduto)
class ClasseProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'descricao',
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


@admin.register(GrupoProduto)
class GrupoProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'classe',
        'descricao',
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'classe',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


@admin.register(SubGrupoProduto)
class SubGrupoProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'classe',
        'grupo',
        'descricao',
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'classe',
        'grupo',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = (
        'sigla',
        'descricao',
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'descricao',
        'subgrupo',
        'unidade',
        'sigla',
        'especifica',
        'numprotheus',
        'ultimoprecocompra',
        'tabela_eventos',
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'subgrupo',
        'unidade',
        'tabela_eventos',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


@admin.register(SubProduto)
class SubProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'produto',
        'descricao',
        'fator',
        'tipofator',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'produto',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
