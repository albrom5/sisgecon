from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
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


class ProcessosCompraList(ListView):
    model = Processo
    template_name = 'processos/processocompra_list.html'


class ProcessoCompraEdit(UpdateView):
    model = Processo
    fields = ['numero_edital', 'modalidade', 'sistema', 'refer_sistema',
              'data_gco', 'status']
    template_name = 'processos/processo_form.html'

    def get_success_url(self):
        return reverse_lazy('processo_detail', args=[self.object.id])
