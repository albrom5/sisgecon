from django.db import transaction
from django.http import JsonResponse

from django.urls import reverse_lazy

from apps.base.custom_views import (
    CustomCreateView, CustomDetailView, CustomUpdateView, CustomListView
)
from apps.base.views import FilteredListView
from apps.compras.filters import SCFilter
from apps.compras.forms import SolicitacaoCompraForm, ItemSCFormset
from apps.compras.models import SolicitacaoCompra
from apps.processos.models import ProcessoCompra


class SolitacaoCompraNova(CustomCreateView):
    form_class = SolicitacaoCompraForm
    template_name = 'compras/sc_form.html'
    permission_codename = 'compras.add_solicitacaocompra'

    def get_context_data(self, **kwargs):
        data = super(SolitacaoCompraNova, self).get_context_data(**kwargs)
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

        return super(SolitacaoCompraNova, self).form_valid(form)

    def get_success_url(self):
        if self.kwargs:
            return reverse_lazy('processo_detail',
                                args=[self.object.processo_id])
        return reverse_lazy('home')


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

    def get_success_url(self):
        return reverse_lazy('sc_detail', args=[self.object.id])


class SCListProcesso(CustomListView):
    permission_codename = 'compras.view_solicitacaocompra'
    queryset = SolicitacaoCompra.objects.filter(processo=None)
    template_name = 'compras/sclist_processo.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['processo'] = self.kwargs['processo_id']
        return data


def vinculasc(request, pk, processo_id):
    processo = ProcessoCompra.objects.get(processo_id=processo_id)
    sc = SolicitacaoCompra.objects.get(id=pk)
    if sc.processo == None:
        sc.processo = processo
        sc.save()
        data = {'msg':
            f'SC {sc.numsc} vinculada ao processo {processo.processo_id.numero_sei}'}
    else:
        sc.processo = None
        sc.save()
        data = {'msg':
                    f'SC {sc.numsc} desvinculada do processo {processo.processo_id.numero_sei}'}
    return JsonResponse(data)
