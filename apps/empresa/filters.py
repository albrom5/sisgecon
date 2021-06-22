import django_filters

from apps.empresa.models import Pessoa


class FornecedorFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')

    ordem = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('nome', 'nome'),
        ),
        # labels do not need to retain order
        field_labels={
        },
    )

    class Meta:
        model = Pessoa
        fields = ['id', 'nome', 'tipo']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True, fornecedor=True)
