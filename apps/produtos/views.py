from .filters import ProdutoFilter
from .models.produtos import Produto
from .forms import ProdutoForm

from apps.base.views import FilteredListView
from apps.base.custom_views import (
    CustomCreateView,
    CustomDetailView,
    CustomUpdateView
)


class ProdutosList(FilteredListView):
    filterset_class = ProdutoFilter
    template_name = 'produtos/produto_list.html'
    queryset = Produto.objects.all()
    paginate_by = 10
    permission_codename = 'produtos.view_produto'


class ProdutoDetail(CustomDetailView):
    model = Produto
    permission_codename = 'produtos.view_produto'


class ProdutoNovo(CustomCreateView):
    form_class = ProdutoForm
    permission_codename = 'produtos.add_produto'
    template_name = 'produtos/produto_form.html'


class ProdutoEdit(CustomUpdateView):
    form_class = ProdutoForm
    permission_codename = 'produtos.change_produto'
    template_name = 'produtos/produto_form.html'
    model = Produto
