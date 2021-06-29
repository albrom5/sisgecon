import django_filters

from apps.contratos.models import ContratoCompra


class ContratoCompraFilter(django_filters.FilterSet):
    objeto = django_filters.CharFilter(lookup_expr='icontains')
    data_ass_ini = django_filters.DateFilter(field_name='data_assinatura',
                                             lookup_expr='gte')
    data_ass_fim = django_filters.DateFilter(field_name='data_assinatura',
                                             lookup_expr='lte')
    fim_vig_ini = django_filters.DateFilter(field_name='data_fim',
                                             lookup_expr='gte')
    fim_vig_fim = django_filters.DateFilter(field_name='data_fim',
                                             lookup_expr='lte')

    ordem = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('objeto', 'objeto'),
            ('numero', 'numero'),
            ('data_fim', 'data_fim'),
            ('data_assinatura', 'data_assinatura'),
        ),
        # labels do not need to retain order
        field_labels={
        },
    )

    class Meta:
        model = ContratoCompra
        fields = ['objeto', 'numero', 'data_assinatura', 'data_fim', 'tipo']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True)
