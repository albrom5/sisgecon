from django import forms

from dal import autocomplete

from .models import SolicitacaoCompra, ItemSC, Pesquisa

from apps.processos.models import Processo
from apps.produtos.models import SubGrupoProduto


class SolicitacaoCompraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        objeto = ''
        if 'processo_id' in kwargs:
            processo_id = kwargs.pop('processo_id')
            processo = Processo.objects.get(id=processo_id)
            objeto = processo.descricao

        super(SolicitacaoCompraForm, self).__init__(*args, **kwargs)
        self.fields['data_emissao'].widget.attrs.update(
            {'class': 'datemask'}
        )
        self.fields['prazo'].widget.attrs.update(
            {'class': 'datemask'}
        )
        if objeto != "":
            self.fields['objeto'].initial = objeto

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


class ConsultaSaldoForm(forms.Form):
    subgrupo = forms.ModelChoiceField(
        queryset=SubGrupoProduto.objects.filter(ativo=True))

    def __init__(self, *args, **kwargs):
        super(ConsultaSaldoForm, self).__init__(*args, **kwargs)
        self.fields['subgrupo'].widget.attrs.update(
            {'class': 'form-select'}
        )


ItemSCFormset = forms.inlineformset_factory(SolicitacaoCompra,
                                            ItemSC, form=ItemSCForm,
                                            extra=1, can_delete=True)


class PesquisaForm(forms.ModelForm):

    class Meta:
        model = Pesquisa
        fields = ['processo', 'responsavel', 'contrato']
