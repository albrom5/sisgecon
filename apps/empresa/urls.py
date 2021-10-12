from django.urls import path
from django.views.decorators.cache import never_cache

from .views import (
    FornecedoresList, FornecedorNovoPJ, FornecedorDetail, FornecedorEdit,
    FornecedorNovoPF
)


urlpatterns = [
    path('fornecedores/', never_cache(FornecedoresList.as_view()),
         name='fornecedores_list'),
    path('fornecedores/<int:pk>', never_cache(FornecedorDetail.as_view()),
         name='fornecedor_detail'),
    path('fornecedores/editar/<int:pk>', FornecedorEdit.as_view(),
         name='fornecedor_edit'),
    path('fornecedores/novo_pj/', FornecedorNovoPJ.as_view(),
         name='fornecedor_novo_pj'),
    path('fornecedores/novo_pf/', FornecedorNovoPF.as_view(),
         name='fornecedor_novo_pf')
]
