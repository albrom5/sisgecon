from django import forms

from dal import autocomplete

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
        fields = ['numsc', 'objeto', 'data_emissao', 'prazo', 'area',
                  'responsavel', 'centro_custo', 'conta_contabil']
        widgets = {
            'area': autocomplete.ModelSelect2(
                url='area_autocomplete',
                attrs={'class': 'form-control',
                       'data-minimum-input-length': 1,
                       }),
            'responsavel': autocomplete.ModelSelect2(
                url='resp_autocomplete',
                attrs={
                       'data-minimum-input-length': 2,
                       }),
            'centro_custo': autocomplete.ModelSelect2(
                url='ccusto_autocomplete',
                attrs={'class': 'form-control',
                       'data-minimum-input-length': 4,
                       }),
            'conta_contabil': autocomplete.ModelSelect2(
                url='ccontabil_autocomplete',
                attrs={'class': 'form-control',
                       'data-minimum-input-length': 4,
                       }),
        }


class ItemSCForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemSCForm, self).__init__(*args, **kwargs)
        self.fields['ord_item'].widget.attrs['readonly'] = True

    class Meta:
        model = ItemSC
        fields = ['ord_item', 'produto', 'descricao', 'quantidade',
                  'valor_unit']
        widgets = {
            'produto': autocomplete.ModelSelect2(
                url='produto_autocomplete',
                attrs={'class': 'form-control',
                       'data-minimum-input-length': 1,
                       }),
        }


ItemSCFormset = forms.inlineformset_factory(SolicitacaoCompra,
                                            ItemSC, form=ItemSCForm,
                                            extra=1, can_delete=True)
