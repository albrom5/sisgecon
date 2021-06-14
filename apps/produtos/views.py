from django.views.generic import DetailView, CreateView, UpdateView

from .filters import ProdutoFilter
from .models.produtos import Produto

from apps.base.views import FilteredListView


class ProdutosList(FilteredListView):
    filterset_class = ProdutoFilter
    template_name = 'produtos/produto_list.html'
    queryset = Produto.objects.all()
    paginate_by = 10
    permission_codename = 'produtos.view_produto'


class ProdutoDetail(DetailView):
    model = Produto


class ProdutoNovo(CreateView):
    model = Produto
    fields = ['descricao', 'unidade', 'sigla', 'subgrupo', 'especifica',
              'numprotheus', 'tabela_eventos']


class ProdutoEdit(UpdateView):
    model = Produto
    fields = ['descricao', 'unidade', 'sigla', 'subgrupo', 'especifica',
              'numprotheus', 'tabela_eventos']
