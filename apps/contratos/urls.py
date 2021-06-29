from django.urls import path
from django.views.decorators.cache import never_cache

from apps.contratos.views import (
    ContratosCompraList, ContratoCompraNovo
)

urlpatterns = [
    # path('<int:processo_id>/nova_sc/', SolicitacaoCompraNova.as_view(),
    #      name='sc_nova_pc'),
    path('compras/contrato_novo/', ContratoCompraNovo.as_view(),
         name='contratocompra_novo'),
    path('compras/', never_cache(ContratosCompraList.as_view()),
         name='contratoscompras_list'),
    # path('sc/<int:pk>', SolicitacaoCompraDetail.as_view(), name='sc_detail'),
    # path('sc/edit/<int:pk>', SolicitacaoCompraEdit.as_view(), name='sc_edit'),
    # path('<int:processo_id>/lista_sc/', never_cache(
    #     SCListProcesso.as_view()), name='sclist_processo'),
    # path('ajax/<int:processo_id>/vincula_sc/<int:pk>', vinculasc,
    #      name='vincula_sc')
]