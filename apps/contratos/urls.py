from django.urls import path
from django.views.decorators.cache import never_cache

from apps.contratos.views import (
    ContratosCompraList, ContratoCompraDetail, ContratoCompraNovo,
    buscafornecedor, buscaprocesso
)

urlpatterns = [
    # path('<int:processo_id>/nova_sc/', SolicitacaoCompraNova.as_view(),
    #      name='sc_nova_pc'),
    path('compras/contrato_novo/', ContratoCompraNovo.as_view(),
         name='contratocompra_novo'),
    path('compras/', never_cache(ContratosCompraList.as_view()),
         name='contratoscompras_list'),
    path('compras/<int:pk>', ContratoCompraDetail.as_view(),
         name='compra_detail'),
    # path('sc/edit/<int:pk>', SolicitacaoCompraEdit.as_view(), name='sc_edit'),
    # path('<int:processo_id>/lista_sc/', never_cache(
    #     SCListProcesso.as_view()), name='sclist_processo'),
    path('ajax/busca_fornecedor/', buscafornecedor,
         name='busca_fornecedor'),
    path('ajax/busca_processo/', buscaprocesso,
         name='busca_processo')
]