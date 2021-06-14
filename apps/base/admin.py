from django.contrib import admin

from .models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tipo',
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
