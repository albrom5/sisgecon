from .filters import FornecedorFilter
from .models.empresas import Pessoa

from apps.base.views import FilteredListView


class FornecedoresList(FilteredListView):
    filterset_class = FornecedorFilter
    template_name = 'empresa/fornecedores_list.html'
    queryset = Pessoa.objects.all()
    paginate_by = 10
    permission_codename = 'empresa.view_pessoa'


