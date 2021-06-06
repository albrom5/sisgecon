from django.contrib import admin

from .models import Modalidade, Sistema, Processo, ProcessoCompra


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
        'data_autuacao',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'data_autuacao',
    )


admin.site.register(ProcessoCompra)