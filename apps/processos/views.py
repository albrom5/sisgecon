import django_filters
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from .models import Processo


class ProcessoCompraNovo(CreateView):
    model = Processo
    fields = ['numero_sei', 'tipo', 'descricao']
    template_name = 'processos/processo_form.html'

    def get_success_url(self):
        return reverse_lazy('processo_detail', args=[self.object.id])


class ProcessoCompraDetail(DetailView):
    model = Processo
    template_name = 'processos/processocompra_detail.html'


# class ProcessosCompraList(ListView):
#     model = Processo
#     template_name = 'processos/processocompra_list.html'

def processo_list(request):
    f = ProcessoFilter(request.GET, queryset=Processo.objects.all())
    return render(request, 'processos/processocompra_list.html', {'filter': f})


class ProcessoCompraEdit(UpdateView):
    model = Processo
    fields = ['numero_edital', 'modalidade', 'sistema', 'refer_sistema',
              'data_gco', 'status']
    template_name = 'processos/processo_form.html'

    def get_success_url(self):
        return reverse_lazy('processo_detail', args=[self.object.id])


class ProcessoFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Processo
        fields = ['numero_sei', 'descricao', 'modalidade', 'status',
                  'data_gco']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(ativo=True)
