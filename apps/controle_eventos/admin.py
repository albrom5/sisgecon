from django.contrib import admin

from .models import OrdemFornecimento, ItemOF, DecomposicaoValor


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