from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models.produtos import Produto


class ProdutosList(ListView):
    model = Produto

    def get_queryset(self):
        return Produto.objects.filter(ativo=True)


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
