import django_filters

from apps.contratos.models import RevisaoContratoCompra, ContratoCompra


class RevisaoContratoCompraFilter(django_filters.FilterSet):
    contrato__numero = django_filters.CharFilter(lookup_expr='iexact')
    contrato__tipo = django_filters.ChoiceFilter(choices=
                                                 ContratoCompra.TIPO_CONTRATO)
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
            ('contrato__numero', 'contrato__numero'),
            # ('data_fim', 'data_fim'),
            ('data_assinatura', 'data_assinatura'),
        ),
        # labels do not need to retain order
        field_labels={
        },
    )

    class Meta:
        model = RevisaoContratoCompra
        fields = ['objeto', 'data_assinatura' ]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True, is_vigente=True)
