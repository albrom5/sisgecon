from django import forms
from .models import SolicitacaoCompra, ItemSC


class SolicitacaoCompraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SolicitacaoCompraForm, self).__init__(*args, **kwargs)
        self.fields['data_emissao'].widget.attrs.update(
            {'class': 'datemask'}
        )
        self.fields['prazo'].widget.attrs.update(
            {'class': 'datemask'}
        )

    class Meta:
        model = SolicitacaoCompra
        fields = ['numsc', 'data_emissao', 'prazo']


class ItemSCForm(forms.ModelForm):

    class Meta:
        model = ItemSC
        fields = ['ord_item', 'produto',
                  'descricao', 'quantidade', 'valor_unit']


ItemSCFormset = forms.inlineformset_factory(SolicitacaoCompra,
                                            ItemSC, form=ItemSCForm,
                                            extra=3)
