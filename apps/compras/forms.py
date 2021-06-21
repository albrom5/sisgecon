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
        self.fields['area'].widget.attrs.update({'class': 'form-select'})
        self.fields['responsavel'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['centro_custo'].widget.attrs.update(
            {'class': 'form-select'})
        self.fields['conta_contabil'].widget.attrs.update(
            {'class': 'form-select'})

    class Meta:
        model = SolicitacaoCompra
        fields = ['numsc', 'objeto', 'data_emissao', 'prazo', 'area',
                  'responsavel', 'centro_custo', 'conta_contabil']


class ItemSCForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemSCForm, self).__init__(*args, **kwargs)
        self.fields['produto'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = ItemSC
        fields = ['ord_item', 'produto',
                  'descricao', 'quantidade', 'valor_unit']


ItemSCFormset = forms.inlineformset_factory(SolicitacaoCompra,
                                            ItemSC, form=ItemSCForm,
                                            extra=1, can_delete=True)
