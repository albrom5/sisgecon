import django_filters

from .models import Produto


class ProdutoFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Produto
        fields = ['sigla', 'descricao', 'subgrupo', 'tabela_eventos']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True)
