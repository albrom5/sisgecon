from django.contrib import admin

from .models import (
    OrdemFornecimento, ItemOF, DecomposicaoValor, SubItemOF, Evento, SubEvento,
)


@admin.register(OrdemFornecimento)
class OrdemFornecimentoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'contrato',
        'numero_format_ano',
        'data_emissao',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'contrato',
    )


@admin.register(ItemOF)
class ItemOFAdmin(admin.ModelAdmin):
    list_display = (
        'ordem_fornecimento',
        'ord_item',
        'produto',
        'quantidade',
        'total_item',
    )


@admin.register(DecomposicaoValor)
class DecomposicaoValorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item',
        'valor_corrigido',
        'dias',
        'subtotal',
    )


@admin.register(SubItemOF)
class SubItemOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item_of',
        'item_contrato',
    )


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'contrato',
        'descricao',
    )


@admin.register(SubEvento)
class SubEvento(admin.ModelAdmin):
    list_display = (
        'id',
        'evento',
        'descricao',
    )
