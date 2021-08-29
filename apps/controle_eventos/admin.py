from django.contrib import admin

from .models import OrdemFornecimento, ItemOF


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
        'valor_unit',
        'valor_total',
    )
