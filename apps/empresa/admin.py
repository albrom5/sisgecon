# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Diretoria, Gerencia, Coordenadoria, Departamento, Cargo, Funcionario


@admin.register(Diretoria)
class DiretoriaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sigla',
        'nome',
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


@admin.register(Gerencia)
class GerenciaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sigla',
        'nome',
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


@admin.register(Coordenadoria)
class CoordenadoriaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sigla',
        'nome',
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


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'diretoria',
        'gerencia',
        'coordenadoria',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'diretoria',
        'gerencia',
        'coordenadoria',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nome',
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


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'departamento',
        'cargo',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )
    list_filter = (
        'user',
        'departamento',
        'cargo',
        'ativo',
        'criado_em',
        'criador',
        'modificado_em',
        'ultimo_editor',
    )

