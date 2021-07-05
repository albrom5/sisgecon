from django import forms
from .models import ContratoCompra, ItemContratoCompra


class ContratoCompraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContratoCompraForm, self).__init__(*args, **kwargs)
        self.fields['data_ini'].widget.attrs.update(
            {'class': 'datemask'}
        )
        self.fields['data_fim'].widget.attrs.update(
            {'class': 'datemask'}
        )
        self.fields['data_assinatura'].widget.attrs.update(
            {'class': 'datemask'}
        )
        self.fields['tipo'].widget.attrs.update(
            {'class': 'form-select'}
        )
        self.fields['fornecedor'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['fornecedor'].widget.attrs['readonly'] = True

    class Meta:
        model = ContratoCompra
        fields = ['numero', 'objeto', 'data_ini', 'data_fim',
                  'data_assinatura', 'area', 'fornecedor', 'tipo']


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
    ContratoCompra,
    ItemContratoCompra,
    form=ItemContratoCompraForm,
    extra=1, can_delete=True
)
