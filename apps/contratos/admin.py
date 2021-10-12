from django.contrib import admin

from .models import (
    ContratoCompra, ItemContratoCompra, RevisaoContratoCompra,
    SubItemContratoCompra, AtaRP, RevisaoAta, ItemAta, SubItemAta
)


@admin.register(ContratoCompra)
class ContratoCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tipo',
        'numero_formatado',
        'numero_formatado_com_tipo',
        'processo',
        'data_assinatura',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'tipo',
        'processo',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


@admin.register(ItemContratoCompra)
class ItemContratoCompraAdmin(admin.ModelAdmin):
    list_display = (
        'ord_item',
        'produto',
        'valor_unit',
        'valor_total',
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


@admin.register(RevisaoContratoCompra)
class RevisaoContratoCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero_formatado',
        'numero_formatado_com_tipo',
        'contrato',
        'ordem',
        'data_assinatura',
        'is_vigente',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'contrato',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


@admin.register(SubItemContratoCompra)
class SubItemContratoCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'descricao',
        'tipofator',
        'fator',
        'diaria_inicial',
    )


@admin.register(AtaRP)
class AtaRPAdmin(admin.ModelAdmin):
    list_display = (
        'numero_format_ano',
        'fornecedor'
    )


@admin.register(RevisaoAta)
class RevisaoAtaAdmin(admin.ModelAdmin):
    list_display = (
        'ata',
        'ordem'
    )


@admin.register(ItemAta)
class ItemAtaAdmin(admin.ModelAdmin):
    list_display = (
        'revisao',
        'ord_item',
    )


@admin.register(SubItemAta)
class SubItemAtaAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'descricao'
    )
