import django_filters

from apps.produtos.models import Produto


class ProdutoFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(lookup_expr='icontains')

    ordem = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('descricao', 'descricao'),
            ('numprotheus', 'numprotheus'),
        ),
        # labels do not need to retain order
        field_labels={
            'descricao': 'Nome',
            'numprotheus': 'Número Protheus',
        },
    )

    class Meta:
        model = Produto
        fields = ['id', 'sigla', 'descricao', 'subgrupo', 'tabela_eventos',
                  'numprotheus']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True)
