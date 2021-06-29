from django.db import transaction
from django.urls import reverse_lazy

from .filters import FornecedorFilter
from .models.empresas import Pessoa, PessoaJuridica, PessoaFisica

from apps.base.views import FilteredListView
from apps.base.custom_views import (
    CustomCreateView, CustomDetailView, CustomUpdateView
)
from .forms import (
    FornecedorPJForm, FornecedorPFForm, ContatoFornFormset,
    ContatoFornPFFormset
)


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


class FornecedorNovoPF(CustomCreateView):
    form_class = FornecedorPFForm
    permission_codename = 'empresa.add_pessoa'
    template_name = 'empresa/fornecedorpfedit_form.html'

    def get_context_data(self, **kwargs):
        data = super(FornecedorNovoPF, self).get_context_data(**kwargs)
        if self.request.POST:
            data['contatos'] = ContatoFornPFFormset(self.request.POST)
        else:
            data['contatos'] = ContatoFornPFFormset()
        return data

    def form_valid(self, form):
        pessoa = form.save(commit=False)
        pessoa.tipo = 'PF'
        pessoa.fornecedor = True
        context = self.get_context_data()
        contatos = context['contatos']
        with transaction.atomic():
            self.object = form.save()
        if contatos.is_valid():
            contatos.instance = self.object
            contatos.save()
        return super(FornecedorNovoPF, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('fornecedores_list')


class FornecedorDetail(CustomDetailView):
    model = Pessoa
    permission_codename = 'empresa.view_pessoa'
    template_name = 'empresa/fornecedor_detail.html'


class FornecedorEdit(CustomUpdateView):
    permission_codename = 'empresa.change_pessoa'

    def get_form_class(self):
        pessoa = self.kwargs['pk']
        fornecedor = Pessoa.objects.get(id=pessoa)
        tipo = fornecedor.tipo
        if tipo == 'PJ':
            form_class = FornecedorPJForm
            return form_class
        else:
            form_class = FornecedorPFForm
            return form_class

    def get_template_names(self):
        pessoa = self.kwargs['pk']
        fornecedor = Pessoa.objects.get(id=pessoa)
        tipo = fornecedor.tipo
        if tipo == 'PJ':
            template_name = 'empresa/fornecedor_form.html'
            return template_name
        else:
            template_name = 'empresa/fornecedorpfedit_form.html'
            return template_name

    def get_queryset(self):
        pessoa = self.kwargs['pk']
        fornecedor = Pessoa.objects.get(id=pessoa)
        tipo = fornecedor.tipo

        if tipo == 'PJ':
            queryset = PessoaJuridica.objects.filter(ativo=True)
            return queryset
        else:
            queryset = PessoaFisica.objects.filter(ativo=True)
            return queryset


    def get_context_data(self, **kwargs):
        data = super(FornecedorEdit, self).get_context_data(**kwargs)
        pessoa = self.kwargs['pk']
        fornecedor = Pessoa.objects.get(id=pessoa)
        tipo = fornecedor.tipo
        if self.request.POST:
            if tipo == 'PJ':
                data['contatos'] = ContatoFornFormset(self.request.POST,
                                                      instance=self.object)
            else:
                data['contatos'] = ContatoFornPFFormset(self.request.POST,
                                                      instance=self.object)
        else:
            if tipo == 'PJ':
                data['contatos'] = ContatoFornFormset(instance=self.object)
            else:
                data['contatos'] = ContatoFornPFFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        contatos = context['contatos']
        with transaction.atomic():
            self.object = form.save()
        if contatos.is_valid():
            contatos.instance = self.object
            contatos.save()
        return super(FornecedorEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('fornecedor_detail', args=[self.object.id])