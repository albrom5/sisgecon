from django.contrib import admin

from .models import Modalidade, Sistema, Processo, ProcessoCompra


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sigla',
        'fundamento',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
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
        'descricao',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
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
        'numero_sei',
        'tipo',
        'descricao',
        'data_autuacao',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'data_autuacao',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


admin.site.register(ProcessoCompra)
