from django import forms

from .models import ProcessoCompra


class ProcessoCompraForm(forms.ModelForm):

    numero_sei = forms.CharField(max_length=19, required=True)
    objeto = forms.CharField(max_length=250)

    # def __init__(self, *args, **kwargs):
    #     if 'instance' in kwargs:
    #         instance = kwargs.pop('instance')
    #         instance = ProcessoCompra.objects.get(pk=instance.pk)
    #         super(ProcessoCompraForm, self).__init__(
    #             instance=instance, *args, **kwargs)
    #     else:
    #         super(ProcessoCompraForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProcessoCompra
        fields = ['modalidade', 'numero_edital', 'sistema', 'refer_sistema',
                  'data_gco', 'status']
