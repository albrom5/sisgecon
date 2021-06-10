from django import forms

from .models import ProcessoCompra, Processo


class ProcessoCompraForm(forms.ModelForm):

    numero_sei = forms.CharField(max_length=19, required=True,
                                 label='Número SEI')
    objeto = forms.CharField(max_length=250)

    def clean(self):
        cleaned_data = super().clean()
        numero = cleaned_data.get("numero_sei")
        qs = Processo.objects.filter(numero_sei=numero)
        if len(numero) < 19:
            msg = "Número de processo deve conter 16 dígitos (Ex.: 7210.2021/0000001-0)"
            self.add_error('numero_sei', msg)

        if qs:
            msg = "Número de processo já cadastrado."
            self.add_error('numero_sei', msg)

    class Meta:
        model = ProcessoCompra
        fields = ['modalidade', 'data_gco', 'status']

# TODO Validar número de processo quando ele for alterado
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
