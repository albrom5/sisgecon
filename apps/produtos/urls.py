from django.urls import path
from django.views.decorators.cache import never_cache

from .views import (
    ProdutoDetail, ProdutoEdit, ProdutoNovo, ProdutosList
)
from .autocomplete_views import (
    SubgrupoAutocomplete
)


urlpatterns = [
    path('', never_cache(ProdutosList.as_view()), name='produtos_list'),
    path('<int:pk>', never_cache(ProdutoDetail.as_view()), name='produto_detail'),
    path('editar/<int:pk>', ProdutoEdit.as_view(), name='produto_edit'),
    path('novo/', ProdutoNovo.as_view(), name='produto_novo'),
    # Autocomplete
    path('subgrupo_autocomplete', SubgrupoAutocomplete.as_view(),
         name='subgrupo_autocomplete')
]
