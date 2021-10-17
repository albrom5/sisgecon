from django.db.models import Q

import django_filters
from django_filters import OrderingFilter

from apps.processos.models import ProcessoCompra
from apps.empresa.models import Funcionario


class ProcessoFilter(django_filters.FilterSet):
    processo_id__numero_sei = django_filters.CharFilter(lookup_expr='iexact')
    processo_id__descricao = django_filters.CharFilter(lookup_expr='icontains')
    data_gco_ini = django_filters.DateFilter(field_name='data_gco',
                                             lookup_expr='gte')
    data_gco_fim = django_filters.DateFilter(field_name='data_gco',
                                             lookup_expr='lte')

    comprador = django_filters.ModelChoiceFilter(
        queryset=Funcionario.objects.filter(Q(ativo=True) & Q(pregoeiro=True))
    )

    ordem = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('processo_id__numero_sei', 'processo_id__numero_sei'),
            ('data_gco', 'data_gco'),
        ),
        # labels do not need to retain order
        field_labels={
            'processo_id__numero_sei': 'Número SEI',
            'data_gco': 'Data de entrada na GCO',
        },
    )

    class Meta:
        model = ProcessoCompra
        fields = ['modalidade', 'status', 'comprador']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True)
