import datetime

from django.db import transaction
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from apps.base.custom_views import (
    CustomCreateView, CustomDetailView, CustomUpdateView, CustomListView
)
from apps.base.views import FilteredListView
from apps.compras.filters import SCFilter
from apps.compras.forms import (
    SolicitacaoCompraForm, ItemSCFormset, ConsultaSaldoForm
)
from apps.contratos.models import RevisaoContratoCompra
from apps.compras.models import SolicitacaoCompra
from apps.processos.models import ProcessoCompra
from apps.produtos.models import SubGrupoProduto

class SolicitacaoCompraNova(CustomCreateView):
    form_class = SolicitacaoCompraForm
    template_name = 'compras/sc_form.html'
    permission_codename = 'compras.add_solicitacaocompra'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        if 'processo_id' in self.kwargs:
            kwargs['processo_id'] = self.kwargs['processo_id']
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(SolicitacaoCompraNova, self).get_context_data(**kwargs)
        if self.request.POST:
            data['itens'] = ItemSCFormset(self.request.POST)
        else:
            data['itens'] = ItemSCFormset()
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
        return super(SolicitacaoCompraNova, self).form_valid(form)

    def get_success_url(self):
        if self.kwargs:
            return reverse_lazy('processo_detail',
                                args=[self.object.processo_id])
        return reverse_lazy('sc_detail', args=[self.object.id])


class SolicitacaoCompraList(FilteredListView):
    filterset_class = SCFilter
    template_name = 'compras/sc_list.html'
    queryset = SolicitacaoCompra.objects.all()
    paginate_by = 10
    permission_codename = 'compras.view_solicitacaocompra'


class SolicitacaoCompraDetail(CustomDetailView):
    model = SolicitacaoCompra
    permission_codename = 'compras.view_solicitacaocompra'
    template_name = 'compras/sc_detail.html'


class SolicitacaoCompraEdit(CustomUpdateView):
    form_class = SolicitacaoCompraForm
    permission_codename = 'compras.change_solicitacaocompra'
    template_name = 'compras/sc_form.html'
    model = SolicitacaoCompra

    def get_context_data(self, **kwargs):
        data = super(SolicitacaoCompraEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['itens'] = ItemSCFormset(
                self.request.POST, instance=self.object
            )
        else:
            data['itens'] = ItemSCFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        itens = context['itens']
        with transaction.atomic():
            self.object = form.save()
        if itens.is_valid():
            itens.instance = self.object
            itens.save()
        return super(SolicitacaoCompraEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('sc_detail', args=[self.object.id])

class SCListProcesso(CustomListView):
    permission_codename = 'compras.view_solicitacaocompra'
    template_name = 'compras/sclist_processo.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['processo'] = self.kwargs['processo_id']
        return data

    def get_queryset(self):
        numpc = self.kwargs['processo_id']
        queryset = SolicitacaoCompra.objects.filter(
            Q(processo=None) | Q(processo__processo_id_id=numpc)).order_by(
            'processo', 'numsc'
        )
        return queryset


def vinculasc(request, pk, processo_id):
    processo = ProcessoCompra.objects.get(processo_id=processo_id)
    sc = SolicitacaoCompra.objects.get(id=pk)
    if not sc.processo:
        sc.processo = processo
        sc.save()
        data = {
            'addmsg': f'SC {sc.numsc} VINCULADA ao processo '
                      f'{processo.processo_id.numero_sei}',
            'remmsg': ''
        }
    else:
        sc.processo = None
        sc.save()
        data = {
            'addmsg': '',
            'remmsg': f'SC {sc.numsc} RETIRADA do processo '
                      f'{processo.processo_id.numero_sei}'}
    return JsonResponse(data)

def consulta_saldo_dl(request):
    template_name = 'compras/consulta_saldo.html'
    form = ConsultaSaldoForm
    context = {}
    subgrupo = request.GET.get('subgrupo')
    context['form'] = form(request.GET)
    processos = ProcessoCompra.objects.filter(
        Q(
            ativo=True,
            subgrupo=subgrupo,
            modalidade__sigla='DL - Art. 29 II',
            status__contabiliza_saldo=True
        ) |
        Q(
            ativo=True,
            subgrupo=subgrupo,
            modalidade__sigla='DL - Art. 29 I',
            status__contabiliza_saldo=True
        )
    ).annotate(
        total=Sum('solicitacaocompra__valor_total'))
    valores_pcs = []
    for pc in processos:
        valores_pcs.append(pc.total)
    context['total_andamento'] = sum(valores_pcs)

    context['processos'] = processos
    data_de_corte = datetime.date.today() - datetime.timedelta(days=30)
    contratos = RevisaoContratoCompra.objects.filter(
        Q(
            ativo=True,
            subgrupo=subgrupo,
            contrato__modalidade__sigla='DL - Art. 29 II',
            data_assinatura__gte=data_de_corte,
            is_vigente=True
        ) |
        Q(
            ativo=True,
            subgrupo=subgrupo,
            contrato__modalidade__sigla='DL - Art. 29 I',
            data_assinatura__gte=data_de_corte,
            is_vigente=True
        )
    )

    context['contratos'] = contratos

    valores_contratos = []
    for contrato in contratos:
        valores_contratos.append(contrato.valor_total)
    context['total_contratado'] = sum(valores_contratos)

    limite_dl = 50000

    if subgrupo:
        classe = SubGrupoProduto.objects.get(id=subgrupo)

        if classe.classe.descricao == 'Serviço de Engenharia':
            limite_dl = 100000

    saldo_disponivel = limite_dl - (sum(valores_contratos) + sum(valores_pcs))
    context['saldo_disponivel'] = saldo_disponivel
    context['hoje'] = datetime.date.today()
    return render(request, template_name, context)
