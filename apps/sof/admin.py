from django.contrib import admin

from .models import (
    OrgaoSOF, UnidadeSOF, FuncaoSOF, SubFuncaoSOF, ProgramaSOF,
    ProjetoAtividadeSOF, CategoriaSOF, GrupoSOF, ModalidadeSOF, ElementoSOF,
    SubElementoSOF, FonteRecursoSOF, Dotacao, Reserva, Empenho, ContratoSof
)

@admin.register(OrgaoSOF)
class OrgaoSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(UnidadeSOF)
class UnidadeSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(FuncaoSOF)
class FuncaoSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(SubFuncaoSOF)
class SubFuncaoSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(ProgramaSOF)
class ProgramaSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(ProjetoAtividadeSOF)
class ProjetoAtividadeSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(CategoriaSOF)
class CategoriaSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(GrupoSOF)
class GrupoSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(ModalidadeSOF)
class ModalidadeSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(ElementoSOF)
class ElementoSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(SubElementoSOF)
class SubElementoSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(FonteRecursoSOF)
class FonteRecursoSOFAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cod',
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


@admin.register(Dotacao)
class DotacaoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'orgao',
        'unidade',
        'funcao',
        'subfuncao',
        'programa',
        'projeto_atividade',
        'categoria',
        'grupo',
        'modalidade',
        'elemento',
        'subelemento',
        'fonte_recurso',
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
        'orgao',
        'unidade',
        'funcao',
        'subfuncao',
        'programa',
        'projeto_atividade',
        'categoria',
        'grupo',
        'modalidade',
        'elemento',
        'subelemento',
        'fonte_recurso',
    )


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero',
        'data_lancamento',
        'valor',
        'dotacao',
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
        'data_lancamento',
        'dotacao',
    )


@admin.register(Empenho)
class EmpenhoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero',
        'data_lancamento',
        'valor',
        'dotacao',
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
        'data_lancamento',
        'dotacao',
    )


@admin.register(ContratoSof)
class ContratoSofAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero',
        'data_lancamento',
        'valor',
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
        'data_lancamento',
    )
