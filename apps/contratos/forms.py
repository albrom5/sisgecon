from django import forms
from .models import ItemContratoCompra, RevisaoContratoCompra
from apps.empresa.models import Pessoa
from apps.processos.models import ProcessoCompra


class ContratoCompraNovoForm(forms.ModelForm):
    numero_contrato = forms.CharField(max_length=19,
                                      label='Número do Contrato',
                                      required=False)
    fornecedor = forms.ModelChoiceField(
        queryset=Pessoa.objects.filter(ativo=True, fornecedor=True)
    )
    processo = forms.ModelChoiceField(
        queryset=ProcessoCompra.objects.filter(ativo=True)
    )

    def __init__(self, *args, **kwargs):
        super(ContratoCompraNovoForm, self).__init__(*args, **kwargs)
        self.fields['numero_contrato'].widget.attrs.update(
            {'class': 'contrmask'}
        )
        self.fields['data_ini'].widget.attrs.update(
            {'class': 'datemask'}
        )
        self.fields['data_fim'].widget.attrs.update(
            {'class': 'datemask'}
        )
        self.fields['data_assinatura'].widget.attrs.update(
            {'class': 'datemask'}
        )
        self.fields['fornecedor'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['fornecedor'].widget.attrs['readonly'] = True

    class Meta:
        model = RevisaoContratoCompra
        fields = ['data_ini', 'data_fim', 'gestor', 'fiscal',
                  'data_assinatura', 'objeto']


class ItemContratoCompraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemContratoCompraForm, self).__init__(*args, **kwargs)
        self.fields['produto'].widget.attrs.update({'class': 'form-select'})
        self.fields['ord_item'].widget.attrs['readonly'] = True

    class Meta:
        model = ItemContratoCompra
        fields = ['ord_item', 'produto', 'descricao', 'quantidade',
                  'valor_unit']


ItemContratoCompraFormset = forms.inlineformset_factory(
    RevisaoContratoCompra,
    ItemContratoCompra,
    form=ItemContratoCompraForm,
    extra=1, can_delete=True
)
