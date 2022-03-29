import datetime

from django.shortcuts import render

from apps.base.custom_views import CustomListView
from apps.contratos.models import RevisaoContratoCompra


def home(request):
    data = {}
    data['usuario'] = request.user
    departamento = request.user.funcionario.departamento
    contratos = RevisaoContratoCompra.objects.filter(
        area=departamento, data_ini__lte=datetime.date.today(),
        data_fim__gte=datetime.date.today()
    ).select_related('contrato', 'contrato__fornecedor')
    data['contratos'] = contratos
    return render(request, 'base/index.html', data)


class FilteredListView(CustomListView):
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET,
                                              queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filter'] = self.filterset
        return context
