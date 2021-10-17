from django.urls import path
from django.views.decorators.cache import never_cache

from apps.compras.views import (
    SolicitacaoCompraNova, SolicitacaoCompraList, SolicitacaoCompraDetail,
    SolicitacaoCompraEdit, SCListProcesso, vinculasc, consulta_saldo_dl
)
from apps.compras.autocomplete_views import (
    AreaAutocomplete, ResponsavelAutocomplete, CentroCustoAutocomplete,
    ContaContabilAutocomplete, ProdutoAutocomplete
)

urlpatterns = [
    path('<int:processo_id>/nova_sc/', SolicitacaoCompraNova.as_view(),
         name='sc_nova_pc'),
    path('sc_nova/', SolicitacaoCompraNova.as_view(), name='sc_nova'),
    path('sc/', never_cache(SolicitacaoCompraList.as_view()), name='sc_list'),
    path('sc/<int:pk>', never_cache(SolicitacaoCompraDetail.as_view()),
         name='sc_detail'),
    path('sc/edit/<int:pk>', SolicitacaoCompraEdit.as_view(), name='sc_edit'),
    path('<int:processo_id>/lista_sc/', never_cache(
        SCListProcesso.as_view()), name='sclist_processo'),
    path('ajax/<int:processo_id>/vincula_sc/<int:pk>', vinculasc,
         name='vincula_sc'),
    path('consulta_saldo_dl/', consulta_saldo_dl, name='consulta_saldo_dl'),

    # Autocomplete
    path('area_autocomplete/', AreaAutocomplete.as_view(),
         name='area_autocomplete'),
    path('responsavel_autocomplete/', ResponsavelAutocomplete.as_view(),
         name='resp_autocomplete'),
    path('centrocusto_autocomplete/', CentroCustoAutocomplete.as_view(),
         name='ccusto_autocomplete'),
    path('contacontabil_autocomplete/', ContaContabilAutocomplete.as_view(),
         name='ccontabil_autocomplete'),
    path('produto_autocomplete/', ProdutoAutocomplete.as_view(),
         name='produto_autocomplete'),
]
