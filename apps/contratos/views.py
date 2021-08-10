from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy

from apps.base.views import FilteredListView
from apps.base.custom_views import CustomCreateView, CustomDetailView
from apps.empresa.models import PessoaJuridica, PessoaFisica
from apps.processos.models import ProcessoCompra
from .models import ContratoCompra, RevisaoContratoCompra
from .filters import RevisaoContratoCompraFilter
from .forms import ContratoCompraNovoForm, ItemContratoCompraFormset


class ContratosCompraList(FilteredListView):
    filterset_class = RevisaoContratoCompraFilter
    template_name = 'contratos/contratoscompra_list.html'
    queryset = RevisaoContratoCompra.objects.all()
    paginate_by = 10
    permission_codename = 'contratos.view_contratocompra'


class ContratoCompraNovo(CustomCreateView):
    form_class = ContratoCompraNovoForm
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
        contrato = form.save(commit=False)
        num_contrato = form.cleaned_data.get('numero_contrato')
        if num_contrato != '':
            num_contrato = int(num_contrato.split('/')[0])
        if self.kwargs:
            processo = self.kwargs['processo_id']
        else:
            processo = form.cleaned_data.get('processo')
        fornecedor = form.cleaned_data.get('fornecedor')
        data_assinatura = form.cleaned_data.get('data_assinatura')
        contrato.contrato = ContratoCompra.objects.create(
            processo=processo, numero=num_contrato,
            fornecedor=fornecedor, tipo='CCN', data_assinatura=data_assinatura,
        )
        contrato.save()
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


class SubstitutivoCompraNovo(CustomCreateView):
    form_class = ContratoCompraNovoForm
    template_name = 'contratos/compra_form.html'
    permission_codename = 'contratos.add_contratocompra'

    def get_context_data(self, **kwargs):
        data = super(SubstitutivoCompraNovo, self).get_context_data(**kwargs)
        data['substitutivo'] = True
        if self.request.POST:
            data['itens'] = ItemContratoCompraFormset(self.request.POST)
        else:
            data['itens'] = ItemContratoCompraFormset()
        return data

    def form_valid(self, form):
        contrato = form.save(commit=False)
        num_contrato = form.cleaned_data.get('numero_contrato')
        if num_contrato != '':
            num_contrato = int(num_contrato.split('/')[0])
        if self.kwargs:
            processo = self.kwargs['processo_id']
        else:
            processo = form.cleaned_data.get('processo')
        fornecedor = form.cleaned_data.get('fornecedor')
        data_assinatura = form.cleaned_data.get('data_assinatura')
        contrato.contrato = ContratoCompra.objects.create(
            processo=processo, numero=num_contrato,
            fornecedor=fornecedor, tipo='CCO', data_assinatura=data_assinatura,
        )
        contrato.save()
        context = self.get_context_data()
        itens = context['itens']
        with transaction.atomic():
            self.object = form.save()
        if itens.is_valid():
            itens.instance = self.object
            itens.save()
        return super(SubstitutivoCompraNovo, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('compra_detail', args=[self.object.id])


class ContratoCompraDetail(CustomDetailView):
    model = RevisaoContratoCompra
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

def buscaprocesso(request):
    num_pc = request.GET.get('processo')
    processo = ''
    if len(num_pc) == 19 or len(num_pc) == 7:
        try:
            processo = ProcessoCompra.objects.get(
                processo_id__numero_sei=num_pc)
        except:
            processo = ''
    else:
        data = {'msg': 'Digite um Número de processo válido.',
                'isvalid': False}
        return JsonResponse(data)
    if processo == '':
        data = {'msg': 'Processo não cadastrado.',
                'isvalid': False}
        return JsonResponse(data)
    pc_objeto = processo.processo_id.descricao
    cod_pc = processo.processo_id.id
    data = {'processo': pc_objeto,
            'cod': cod_pc,
            'isvalid': True}
    return JsonResponse(data)
