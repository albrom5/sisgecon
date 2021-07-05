from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy

from apps.base.views import FilteredListView
from apps.base.custom_views import CustomCreateView, CustomDetailView
from apps.empresa.models import PessoaJuridica, PessoaFisica
from .models import ContratoCompra
from .filters import ContratoCompraFilter
from .forms import ContratoCompraForm, ItemContratoCompraFormset


class ContratosCompraList(FilteredListView):
    filterset_class = ContratoCompraFilter
    template_name = 'contratos/contratoscompra_list.html'
    queryset = ContratoCompra.objects.all()
    paginate_by = 10
    permission_codename = 'contratos.view_contratocompra'


class ContratoCompraNovo(CustomCreateView):
    form_class = ContratoCompraForm
    template_name = 'contratos/compra_form.html'
    permission_codename = 'contratos.add_contratocompra'

    def get_context_data(self, **kwargs):
        data = super(ContratoCompraNovo, self).get_context_data(**kwargs)
        if self.request.POST:
            data['itens'] = ItemContratoCompraFormset(self.request.POST)
        else:
            data['itens'] = ItemContratoCompraFormset()
        return data

    def form_valid(self, form):
        if self.kwargs:
            form.instance.processo_id = self.kwargs['processo_id']
        context = self.get_context_data()
        itens = context['itens']
        with transaction.atomic():
            self.object = form.save()
        if itens.is_valid():
            itens.instance = self.object
            itens.save()
        return super(ContratoCompraNovo, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('compra_detail', args=[self.object.id])


class ContratoCompraDetail(CustomDetailView):
    model = ContratoCompra
    permission_codename = 'contratos.view_contratocompra'
    template_name = 'contratos/compra_detail.html'


def buscafornecedor(request):
    cnpj_cpf = request.GET.get('cnpj_cpf')
    fornecedor = ''
    if len(cnpj_cpf) == 18:
        try:
            fornecedor = PessoaJuridica.objects.get(cnpj=cnpj_cpf)
        except:
            fornecedor = ''
    elif len(cnpj_cpf) == 14:
        try:
            fornecedor = PessoaFisica.objects.get(cpf=cnpj_cpf)
        except:
            fornecedor = ''
    else:
        data = {'msg': 'Digite um CNPJ ou CPF válido.',
                'isvalid': False}
        return JsonResponse(data)
    if fornecedor == '':
        data = {'msg': 'Fornecedor não cadastrado.',
                'isvalid': False}
        return JsonResponse(data)
    nome = fornecedor.nome
    codigo = fornecedor.id
    data = {'fornecedor': nome,
            'cod': codigo,
            'isvalid': True}
    return JsonResponse(data)
