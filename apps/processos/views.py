import django_filters
from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django_filters import OrderingFilter
from django.forms import widgets
from .models import Processo, ProcessoCompra
from .forms import ProcessoCompraForm
from apps.base.views import FilteredListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_filters.views import FilterView


class ProcessoCompraNovo(CreateView):
    form_class = ProcessoCompraForm
    template_name = 'processos/processo_form.html'

    def form_valid(self, form):
        processo_compra = form.save(commit=False)
        numero_sei = form.cleaned_data.get('numero_sei')
        descricao = form.cleaned_data.get('objeto')
        processo_compra.processo_id = Processo.objects.create(
            numero_sei=numero_sei, tipo='PC', descricao=descricao)
        processo_compra.save()
        return super(ProcessoCompraNovo, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('processo_detail',
                            args=[self.object.processo_id.id])


class ProcessoCompraDetail(DetailView):
    model = ProcessoCompra
    template_name = 'processos/processocompra_detail.html'


# class ProcessosCompraList(ListView):
#     model = Processo
#     template_name = 'processos/processocompra_list.html'

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


class ProcessoFilter(django_filters.FilterSet):
    processo_id__numero_sei = django_filters.CharFilter(lookup_expr='iexact')
    processo_id__descricao = django_filters.CharFilter(lookup_expr='icontains')
    ordem = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('processo_id__numero_sei', 'processo_id__numero_sei'),
            ('data_gco', 'data_gco'),
        ),
        # labels do not need to retain order
        field_labels={
            'processo_id__numero_sei': 'Número SEI',
            'data_gco': 'Data de entrada na GCO',
        },
    )

    class Meta:
        model = ProcessoCompra
        fields = ['modalidade', 'status', 'data_gco']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True)


# class ProcessosCompraList(FilterView):
#     filterset_class = ProcessoFilter
#     template_name = 'processos/processocompra_list.html'

class ProcessosCompraList(FilteredListView):
    filterset_class = ProcessoFilter
    template_name = 'processos/processocompra_list.html'
    queryset = ProcessoCompra.objects.all()
    paginate_by = 5
