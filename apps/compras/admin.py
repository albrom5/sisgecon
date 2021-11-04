from django.contrib import admin

from .models import (
    SolicitacaoCompra, ItemSC, Pregao, Lote, ItemLote, Pesquisa, Proposta,
    ItemProposta, ItemPesquisa
)


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


@admin.register(Pregao)
class PregaoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_edital',
        'processo'
    )


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = (
        'pregao',
        'numero'
    )


@admin.register(ItemLote)
class ItemLoteAdmin(admin.ModelAdmin):
    list_display = (
        'lote',
        'produto'
    )


admin.site.register(Pesquisa)

admin.site.register(Proposta)

admin.site.register(ItemProposta)

admin.site.register(ItemPesquisa)