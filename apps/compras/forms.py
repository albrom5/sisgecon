from django import forms

from .models import SolicitacaoCompra


class SolicitacaoCompraForm(forms.ModelForm):

    class Meta:
        model = SolicitacaoCompra
        fields = ['numsc', 'data_emissao', 'prazo']
