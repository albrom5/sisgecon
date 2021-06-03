from django.contrib import admin

from .models import SolicitacaoCompra, ItemSC


@admin.register(SolicitacaoCompra)
class SolicitacaoCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'numsc',
        'data_emissao',
        'prazo',
        'data_rec_compras',
        'processo',
        'objeto',
        'justificativa',
        'valor_total',
        'centro_custo',
        'conta_contabil',
        'contr_evento',
        'evento',
        'cadtec',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'data_emissao',
        'prazo',
        'data_rec_compras',
        'processo',
    )


@admin.register(ItemSC)
class ItemSCAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'solicitacao',
        'ord_item',
        'subgrupo',
        'produto',
        'descricao',
        'quantidade',
        'diaria',
        'valor_unit',
        'valor_total',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'solicitacao',
        'subgrupo',
        'produto',
    )
