from django.urls import path
from .views import ProcessoCompraNovo


urlpatterns = [
    path('processo/novo', ProcessoCompraNovo.as_view(), name='processo_novo'),
    # path('<int:pk>', ProdutoDetail.as_view(), name='produto_detail'),
    # path('editar/<int:pk>', ProdutoEdit.as_view(), name='produto_edit'),
    # path('novo/', ProdutoNovo.as_view(), name='produto_novo')
]
