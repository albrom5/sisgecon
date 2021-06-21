import django_filters

from apps.compras.models import SolicitacaoCompra


class SCFilter(django_filters.FilterSet):

    item = django_filters.CharFilter()

    data_emis_ini = django_filters.DateFilter(field_name='data_emissao',
                                             lookup_expr='gte')
    data_emis_fim = django_filters.DateFilter(field_name='data_emissao',
                                             lookup_expr='lte')

    ordem = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('numsc', 'numsc'),
            ('data_emissao', 'data_emissao'),
        ),
        # labels do not need to retain order
        field_labels={
            'numsc': 'Número',
        },
    )

    class Meta:
        model = SolicitacaoCompra
        fields = ['numsc', 'data_emissao']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True)
