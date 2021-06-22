from django.urls import path
from django.views.decorators.cache import never_cache

from .views import FornecedoresList


urlpatterns = [
    path('fornecedores/', never_cache(FornecedoresList.as_view()), name='fornecedores_list'),
    # path('<int:pk>', ProdutoDetail.as_view(), name='produto_detail'),
    # path('editar/<int:pk>', ProdutoEdit.as_view(), name='produto_edit'),
    # path('novo/', ProdutoNovo.as_view(), name='produto_novo')
]
