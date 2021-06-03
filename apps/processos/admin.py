from django.contrib import admin

from .models import Modalidade, Sistema, Processo


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'sigla',
        'fundamento',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


@admin.register(Sistema)
class SistemaAdmin(admin.ModelAdmin):
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


@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'numero_sei',
        'tipo',
        'descricao',
        'modalidade',
        'numero_edital',
        'sistema',
        'refer_sistema',
        'data_autuacao',
        'data_gco',
        'status',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'modalidade',
        'sistema',
        'data_autuacao',
        'data_gco',
        'status',
    )

