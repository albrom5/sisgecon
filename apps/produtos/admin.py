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
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'descricao',
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
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'classe',
        'descricao',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'classe',
    )


@admin.register(SubGrupoProduto)
class SubGrupoProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'classe',
        'grupo',
        'descricao',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'classe',
        'grupo',
    )


@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'sigla',
        'descricao',
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
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'descricao',
        'subgrupo',
        'unidade',
        'sigla',
        'especifica',
        'numprotheus',
        'ultimoprecocompra',
        'tabela_eventos',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'subgrupo',
        'unidade',
        'tabela_eventos',
    )


@admin.register(SubProduto)
class SubProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'produto',
        'descricao',
        'fator',
        'tipofator',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'produto',
    )
