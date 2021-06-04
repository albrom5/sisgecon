from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .filters import ProdutoFilter
from .models.produtos import Produto


# class ProdutosList(ListView):
#     model = Produto
#
#     def get_queryset(self):
#         return Produto.objects.filter(ativo=True)

def produto_list(request):
    f = ProdutoFilter(request.GET, queryset=Produto.objects.all())
    return render(request, 'produtos/produto_list.html', {'filter': f})


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
