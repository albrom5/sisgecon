from django.urls import reverse_lazy

from apps.base.custom_views import CustomCreateView
from apps.compras.forms import SolicitacaoCompraForm


class SolitacaoCompraNova(CustomCreateView):
    form_class = SolicitacaoCompraForm
    template_name = 'compras/scnova_form.html'
    permission_codename = 'compras.add_solicitacaocompra'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.processo_id = self.kwargs['processo_id']

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('processo_detail',
                            args=[self.object.processo_id])
