from django.contrib import admin
from .models import (
    ClasseProduto,
    GrupoProduto,
    SubGrupoProduto,
    UnidadeMedida,
    Produto,
    SubProduto,
)

class ClassesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['descricao', 'ativo']}),
    ]
    list_display = ('descricao', 'ativo', 'criado_em','criador', 'modificado_em','ultimo_editor')
    list_filter = ['descricao']

class SubgruposInline(admin.TabularInline):
    model = SubGrupoProduto
    extra = 0
    exclude =['modificado_em']

class GruposAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['classe', 'descricao','ativo']}),
    ]
    inlines = [SubgruposInline]
    list_display = ('descricao','classe', 'ativo', 'criado_em','criador', 'modificado_em','ultimo_editor')
    list_filter = ['classe']


class SubGruposAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['classe', 'grupo','descricao','ativo']}),
    ]
    list_display = ('descricao','classe', 'grupo','ativo', 'criado_em','criador', 'modificado_em','ultimo_editor')
    list_filter = ['classe','grupo']


class UnidadeMedidaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['sigla','descricao','ativo']}),
    ]
    list_display = ('sigla', 'descricao', 'ativo','criado_em','criador', 'modificado_em','ultimo_editor')
    list_filter = ['sigla']

class SubprodutosInline(admin.TabularInline):
    model = SubProduto
    extra = 0
    exclude =['modificado_em']

class ProdutosAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['descricao','subgrupo', 'unidade', 'sigla', 'especifica','numprotheus',
                                        'ultimoprecocompra','tabela_eventos', 'ativo']}),
    ]
    inlines = [SubprodutosInline]
    list_display = ('id','descricao', 'subgrupo','ativo', 'criado_em','criador', 'modificado_em','ultimo_editor')
    list_filter = ['subgrupo']

admin.site.register(ClasseProduto, ClassesAdmin)
admin.site.register(GrupoProduto, GruposAdmin)
admin.site.register(SubGrupoProduto, SubGruposAdmin)
admin.site.register(UnidadeMedida, UnidadeMedidaAdmin)
admin.site.register(Produto, ProdutosAdmin)
