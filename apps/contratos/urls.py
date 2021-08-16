from django.urls import path
from django.views.decorators.cache import never_cache

from apps.contratos.views import (
    ContratosCompraList, ContratoCompraDetail, ContratoCompraNovo,
    SubstitutivoCompraNovo, ContratoCompraEdit, RevisaContratoCompra,
    buscafornecedor, buscaprocesso
)

urlpatterns = [
    path('compras/contrato_novo/', ContratoCompraNovo.as_view(),
         name='contratocompra_novo'),
    path('compras/substitutivo_novo/', SubstitutivoCompraNovo.as_view(),
         name='substitutivo_novo'),
    path('compras/', never_cache(ContratosCompraList.as_view()),
         name='contratoscompras_list'),
    path('compras/<int:pk>', ContratoCompraDetail.as_view(),
         name='compra_detail'),
    path('compras/edit/<int:pk>', ContratoCompraEdit.as_view(),
         name='contratocompra_edit'),
    path('compras/<int:pk>/novo_aditamento/', RevisaContratoCompra.as_view(),
         name='novo_aditamento_compra'),
    path('ajax/busca_fornecedor/', buscafornecedor,
         name='busca_fornecedor'),
    path('ajax/busca_processo/', buscaprocesso,
         name='busca_processo')
]
