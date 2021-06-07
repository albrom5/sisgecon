from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .filters import ProcessoFilter
from .models import Processo, ProcessoCompra, Modalidade
from .forms import ProcessoCompraForm
from apps.base.views import FilteredListView
from apps.base.models import Status


class ProcessoCompraNovo(CreateView):
    form_class = ProcessoCompraForm
    template_name = 'processos/processo_form.html'

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


class ProcessoCompraDetail(DetailView):
    model = ProcessoCompra
    template_name = 'processos/processocompra_detail.html'


# def processo_list(request):
#     f = ProcessoFilter(request.GET, queryset=ProcessoCompra.objects.all())
#     paginator = Paginator(f, 1)
#     page = request.GET.get('page')
#     # page_obj = paginator.get_page(page_number)
#     try:
#         response = paginator.page(page)
#     except PageNotAnInteger:
#         response = paginator.page(1)
#     except EmptyPage:
#         response = paginator.page(paginator.num_pages)
#     # return render(request, 'processos/processocompra_list.html', {'filter': f})
#     return render(request, 'processos/processocompra_list.html', {'filter': response})

class ProcessoCompraEdit(UpdateView):
    form_class = ProcessoCompraForm
    template_name = 'processos/processo_form.html'

    def get_success_url(self):
        return reverse_lazy('processo_detail', args=[self.object.id])

# class ProcessosCompraList(FilterView):
#     filterset_class = ProcessoFilter
#     template_name = 'processos/processocompra_list.html'


class ProcessosCompraList(FilteredListView):
    filterset_class = ProcessoFilter
    template_name = 'processos/processocompra_list.html'
    queryset = ProcessoCompra.objects.all()
    paginate_by = 5
