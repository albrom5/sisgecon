from django.urls import reverse_lazy

from .filters import ProcessoFilter
from .models import Processo, ProcessoCompra, Modalidade
from .forms import ProcessoCompraForm, ProcessoCompraEditForm
from apps.base.views import FilteredListView
from apps.base.models import Status
from apps.base.custom_views import (
    CustomCreateView,
    CustomDetailView,
    CustomUpdateView
)

# TODO Fazer consulta Ajax para saber se o número de Processo ou SC já existe
class ProcessoCompraNovo(CustomCreateView):
    form_class = ProcessoCompraForm
    template_name = 'processos/processocompra_form.html'
    permission_codename = 'processos.add_processocompra'

    def form_valid(self, form):
        processo_compra = form.save(commit=False)
        numero_sei = form.cleaned_data.get('numero_sei')
        descricao = form.cleaned_data.get('objeto')
        processo_compra.processo_id = Processo.objects.create(
            numero_sei=numero_sei, tipo='PC', descricao=descricao)
        processo_compra.status = Status.objects.get(tipo='PC',
                                                    descricao='Inicial')
        processo_compra.modalidade = Modalidade.objects.get(sigla='Indefinida')
        processo_compra.save()
        return super(ProcessoCompraNovo, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('processo_detail',
                            args=[self.object.processo_id.id])


class ProcessoCompraDetail(CustomDetailView):
    model = ProcessoCompra
    template_name = 'processos/processocompra_detail.html'
    permission_codename = 'processos.view_processocompra'


class ProcessoCompraEdit(CustomUpdateView):
    model = ProcessoCompra
    form_class = ProcessoCompraEditForm
    template_name = 'processos/processocompraedit_form.html'
    permission_codename = 'processos.change_processocompra'

    def form_valid(self, form):
        processo_compra = form.save(commit=False)
        numero_sei = form.cleaned_data.get('numero_sei')
        descricao = form.cleaned_data.get('objeto')
        processo = Processo.objects.get(id=processo_compra.processo_id.id)
        processo.numero_sei = numero_sei
        processo.descricao = descricao
        processo.save()
        processo_compra.save()
        return super(ProcessoCompraEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('processo_detail', args=[self.object.processo_id.id])


class ProcessosCompraList(FilteredListView):
    filterset_class = ProcessoFilter
    template_name = 'processos/processocompra_list.html'
    queryset = ProcessoCompra.objects.all()
    paginate_by = 10
    permission_codename = 'processos.view_processocompra'


