from django.db import transaction
from django.urls import reverse_lazy

from .filters import FornecedorFilter
from .models.empresas import Pessoa

from apps.base.views import FilteredListView
from apps.base.custom_views import CustomCreateView
from .forms import FornecedorPJForm, ContatoFornFormset


class FornecedoresList(FilteredListView):
    filterset_class = FornecedorFilter
    template_name = 'empresa/fornecedores_list.html'
    queryset = Pessoa.objects.all()
    paginate_by = 10
    permission_codename = 'empresa.view_pessoa'


class FornecedorNovoPJ(CustomCreateView):
    form_class = FornecedorPJForm
    permission_codename = 'empresa.add_pessoa'
    template_name = 'empresa/fornecedor_form.html'

    def get_context_data(self, **kwargs):
        data = super(FornecedorNovoPJ, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contatos'] = ContatoFornFormset(self.request.POST)
        else:
            data['contatos'] = ContatoFornFormset()
        return data

    def form_valid(self, form):
        pessoa = form.save(commit=False)
        pessoa.tipo = 'PJ'
        pessoa.fornecedor = True
        context = self.get_context_data()
        contatos = context['contatos']
        with transaction.atomic():
            self.object = form.save()
        if contatos.is_valid():
            contatos.instance = self.object
            contatos.save()
        return super(FornecedorNovoPJ, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('fornecedores_list')
