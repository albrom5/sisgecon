from django.contrib import admin

from .models import ContratoCompra, ItemContratoCompra


@admin.register(ContratoCompra)
class ContratoCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tipo',
        'numero',
        'processo',
        'objeto',
        'data_assinatura',
        'valor_total',
        'area',
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
        'contrato',
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
        'contrato',
        'produto',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
