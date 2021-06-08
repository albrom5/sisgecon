from django import forms

from .models import ProcessoCompra


class ProcessoCompraForm(forms.ModelForm):

    numero_sei = forms.CharField(max_length=19, required=True,
                                 label='Número SEI')
    objeto = forms.CharField(max_length=250)

    class Meta:
        model = ProcessoCompra
        fields = ['modalidade', 'data_gco', 'status']


class ProcessoCompraEditForm(forms.ModelForm):
    numero_sei = forms.CharField(max_length=19, required=True,
                                 label='Número SEI')
    objeto = forms.CharField(max_length=250)

    def __init__(self, *args, **kwargs):
        super(ProcessoCompraEditForm, self).__init__(*args, **kwargs)
        processo = kwargs.get('instance')
        numero_sei = processo.processo_id.numero_sei
        objeto = processo.processo_id.descricao
        self.fields['numero_sei'].initial = numero_sei
        self.fields['objeto'].initial = objeto

    class Meta:
        model = ProcessoCompra
        fields = ['modalidade', 'data_gco', 'status']
