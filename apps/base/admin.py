from django.contrib import admin

from .models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
        'tipo',
        'descricao',
    )
    list_filter = (
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
