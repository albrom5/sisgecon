from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy

from apps.base.views import FilteredListView
from apps.base.custom_views import (
    CustomCreateView, CustomDetailView, CustomUpdateView
)
from apps.empresa.models import PessoaJuridica, PessoaFisica
from apps.processos.models import ProcessoCompra, Processo
from apps.controle_eventos.models import OrdemFornecimento
from .models import ContratoCompra, RevisaoContratoCompra
from .filters import RevisaoContratoCompraFilter
from .forms import (
    ContratoCompraNovoForm, ItemContratoCompraFormset, ContratoCompraEditForm,
    RevisaContratoCompraForm
)


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        if 'processo_id' in self.kwargs:
            kwargs['processo_id'] = self.kwargs['processo_id']
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(ContratoCompraNovo, self).get_context_data(**kwargs)
        if self.request.POST:
            data['itens'] = ItemContratoCompraFormset(self.request.POST)
        else:
            data['itens'] = ItemContratoCompraFormset()
            if 'processo_id' in self.kwargs:
                processo_id = self.kwargs['processo_id']
                processo = Processo.objects.get(id=processo_id)
                data['num_pc'] = processo.numero_sei
                data['descricao_pc'] = processo.descricao
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        if 'processo_id' in self.kwargs:
            kwargs['processo_id'] = self.kwargs['processo_id']
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(SubstitutivoCompraNovo, self).get_context_data(**kwargs)
        data['substitutivo'] = True
        if self.request.POST:
            data['itens'] = ItemContratoCompraFormset(self.request.POST)
        else:
            data['itens'] = ItemContratoCompraFormset()
            if 'processo_id' in self.kwargs:
                processo_id = self.kwargs['processo_id']
                processo = Processo.objects.get(id=processo_id)
                data['num_pc'] = processo.numero_sei
                data['descricao_pc'] = processo.descricao
        return data

    def form_valid(self, form):
        contrato = form.save(commit=False)
        num_contrato = form.cleaned_data.get('numero_contrato')
        if num_contrato != '':
            num_contrato = int(num_contrato.split('/')[0])
        # if self.kwargs:
        #     processo = self.kwargs['processo_id']
        # else:
        #     processo = form.cleaned_data.get('processo')
        processo = form.cleaned_data.get('processo')
        fornecedor = form.cleaned_data.get('fornecedor')
        data_assinatura = form.cleaned_data.get('data_assinatura')
        subtipo = form.cleaned_data.get('subtipo')
        contrato.contrato = ContratoCompra.objects.create(
            processo=processo, numero=num_contrato,
            fornecedor=fornecedor, tipo='CCO', subtipo=subtipo,
            data_assinatura=data_assinatura,
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

    def get_context_data(self, **kwargs):
        data = super(ContratoCompraDetail, self).get_context_data(**kwargs)
        num_revisao = self.kwargs['pk']
        revisao = RevisaoContratoCompra.objects.get(id=num_revisao)
        ofs = OrdemFornecimento.objects.filter(
            contrato__contrato_id=revisao.contrato.id
        )
        data['ordens_fornecimento'] = ofs
        return data


class ContratoCompraEdit(CustomUpdateView):
    model = RevisaoContratoCompra
    permission_codename = 'contratos.change_contratocompra'
    form_class = ContratoCompraEditForm
    template_name = 'contratos/compraedit_form.html'

    def get_context_data(self, **kwargs):
        data = super(ContratoCompraEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['itens'] = ItemContratoCompraFormset(
                self.request.POST,
                instance=self.object
            )
        else:
            data['itens'] = ItemContratoCompraFormset(instance=self.object)
        return data

    def form_valid(self, form):
        revisao = form.save(commit=False)
        num_contrato = form.cleaned_data.get('numero_contrato')

        num_contrato = int(num_contrato.split('/')[0])
        processo = form.cleaned_data.get('processo')
        fornecedor = form.cleaned_data.get('fornecedor')
        contrato = ContratoCompra.objects.get(id=revisao.contrato.id)
        contrato.numero = num_contrato
        contrato.processo = processo
        contrato.fornecedor = fornecedor
        contrato.save()
        revisao.save()
        context = self.get_context_data()
        itens = context['itens']
        with transaction.atomic():
            self.object = form.save()
        if itens.is_valid():
            itens.instance = self.object
            itens.save()
        return super(ContratoCompraEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('compra_detail', args=[self.object.id])


class RevisaContratoCompra(CustomCreateView):
    form_class = RevisaContratoCompraForm
    template_name = 'contratos/revisacompra_form.html'
    permission_codename = 'contratos.add_revisaocontratocompra'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        kwargs['contrato_id'] = self.kwargs['contrato_id']
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(RevisaContratoCompra, self).get_context_data(**kwargs)
        contrato_id = self.kwargs['contrato_id']
        revisao_anterior = RevisaoContratoCompra.objects.get(
            contrato=contrato_id, is_vigente=True)
        data['numero_contrato'] = revisao_anterior.contrato.numero_formatado
        data['numero_contrato_com_tipo'] = revisao_anterior.contrato.numero_formatado_com_tipo
        data['processo'] = revisao_anterior.contrato.processo
        data['fornecedor'] = revisao_anterior.contrato.fornecedor
        data['ordem_aditamento'] = revisao_anterior.ordem + 1
        return data

    def form_valid(self, form):
        aditamento = form.save(commit=False)
        num_aditamento = form.cleaned_data.get('numero_aditamento')
        if num_aditamento != '':
            num_aditamento = int(num_aditamento.split('/')[0])
        else:
            num_aditamento = None
        aditamento.numero_aditamento = num_aditamento
        contrato = self.kwargs['contrato_id']
        aditamento.contrato = ContratoCompra.objects.get(id=contrato)

        return super(RevisaContratoCompra, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contratocompra_edit', args=[self.object.id])


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
        data = {'msg': 'Digite um CNPJ ou CPF v??lido.',
                'isvalid': False}
        return JsonResponse(data)
    if fornecedor == '':
        data = {'msg': 'Fornecedor n??o cadastrado.',
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
        data = {'msg': 'Digite um N??mero de processo v??lido.',
                'isvalid': False}
        return JsonResponse(data)
    if processo == '':
        data = {'msg': 'Processo n??o cadastrado.',
                'isvalid': False}
        return JsonResponse(data)
    pc_objeto = processo.processo_id.descricao
    cod_pc = processo.processo_id.id
    data = {'processo': pc_objeto,
            'cod': cod_pc,
            'isvalid': True}
    return JsonResponse(data)
