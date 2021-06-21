from django.urls import path
from django.views.decorators.cache import never_cache

from apps.compras.views import (
    SolitacaoCompraNova, SolicitacaoCompraList, SolicitacaoCompraDetail,
    SolicitacaoCompraEdit, SCListProcesso, vinculasc
)

urlpatterns = [
    path('<int:processo_id>/nova_sc/', SolitacaoCompraNova.as_view(),
         name='sc_nova_pc'),
    path('sc_nova/', SolitacaoCompraNova.as_view(), name='sc_nova'),
    path('sc/', never_cache(SolicitacaoCompraList.as_view()), name='sc_list'),
    path('sc/<int:pk>', SolicitacaoCompraDetail.as_view(), name='sc_detail'),
    path('sc/edit/<int:pk>', SolicitacaoCompraEdit.as_view(), name='sc_edit'),
    path('<int:processo_id>/lista_sc/', never_cache(
        SCListProcesso.as_view()), name='sclist_processo'),
    path('ajax/<int:processo_id>/vincula_sc/<int:pk>', vinculasc,
         name='vincula_sc')
]
