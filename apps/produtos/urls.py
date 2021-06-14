from django.urls import path

from .views import ProdutoDetail, ProdutoEdit, ProdutoNovo, ProdutosList


urlpatterns = [
    path('', ProdutosList.as_view(), name='produtos_list'),
    path('<int:pk>', ProdutoDetail.as_view(), name='produto_detail'),
    path('editar/<int:pk>', ProdutoEdit.as_view(), name='produto_edit'),
    path('novo/', ProdutoNovo.as_view(), name='produto_novo')
]
