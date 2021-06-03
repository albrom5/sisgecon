import django_filters
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
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


class ProdutoFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Produto
        fields = ['sigla', 'descricao', 'subgrupo', 'tabela_eventos']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True)
