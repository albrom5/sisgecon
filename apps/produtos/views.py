from .filters import ProdutoFilter
from .models.produtos import Produto
from .forms import ProdutoForm

from apps.base.views import FilteredListView
from apps.base.custom_views import (
    CustomCreateView,
    CustomDetailView,
    CustomUpdateView
)

from apps.contratos.models import ItemContratoCompra


class ProdutosList(FilteredListView):
    filterset_class = ProdutoFilter
    template_name = 'produtos/produto_list.html'
    queryset = Produto.objects.all()
    paginate_by = 10
    permission_codename = 'produtos.view_produto'


class ProdutoDetail(CustomDetailView):
    model = Produto
    permission_codename = 'produtos.view_produto'

    def get_context_data(self, **kwargs):
        data = super(ProdutoDetail, self).get_context_data(**kwargs)
        produto = self.kwargs['pk']
        contratos = ItemContratoCompra.objects.filter(produto_id=produto,
                                                      revisao__is_vigente=True)
        data['contratos'] = contratos
        return data


class ProdutoNovo(CustomCreateView):
    form_class = ProdutoForm
    permission_codename = 'produtos.add_produto'
    template_name = 'produtos/produto_form.html'


class ProdutoEdit(CustomUpdateView):
    form_class = ProdutoForm
    permission_codename = 'produtos.change_produto'
    template_name = 'produtos/produto_form.html'
    model = Produto
