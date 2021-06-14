from django.db import transaction
from django.urls import reverse_lazy

from apps.base.custom_views import CustomCreateView
from apps.compras.forms import SolicitacaoCompraForm, ItemSCFormset


class SolitacaoCompraNova(CustomCreateView):
    form_class = SolicitacaoCompraForm
    template_name = 'compras/scnova_form.html'
    permission_codename = 'compras.add_solicitacaocompra'

    def get_context_data(self, **kwargs):
        data = super(SolitacaoCompraNova, self).get_context_data(**kwargs)
        if self.request.POST:
            data['itens'] = ItemSCFormset(self.request.POST)
        else:
            data['itens'] = ItemSCFormset()
        return data

    def form_valid(self, form):
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
        return reverse_lazy('processo_detail',
                            args=[self.object.processo_id])
