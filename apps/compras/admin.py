from django.contrib import admin

from .models import SolicitacaoCompra, ItemSC


@admin.register(SolicitacaoCompra)
class SolicitacaoCompraAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numsc',
        'processo',
        'objeto',
        'data_emissao',
        'prazo',
        'data_rec_compras',
        'justificativa',
        'valor_total',
        'centro_custo',
        'conta_contabil',
        'contr_evento',
        'evento',
        'cadtec',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'processo',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'data_emissao',
        'prazo',
        'data_rec_compras',
    )


@admin.register(ItemSC)
class ItemSCAdmin(admin.ModelAdmin):
    list_display = (
        'solicitacao',
        'ord_item',
        'subgrupo',
        'produto',
        'descricao',
        'quantidade',
        'diaria',
        'valor_unit',
        'valor_total',
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'solicitacao',
        'subgrupo',
        'produto',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
