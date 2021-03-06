from django import forms

from dal import autocomplete

from .models import ItemContratoCompra, RevisaoContratoCompra, ContratoCompra
from apps.empresa.models import Pessoa
from apps.processos.models import ProcessoCompra, Processo


class ContratoCompraNovoForm(forms.ModelForm):
    numero_contrato = forms.CharField(max_length=19,
                                      label='Número',
                                      required=False)
    fornecedor = forms.ModelChoiceField(
        queryset=Pessoa.objects.filter(ativo=True, fornecedor=True)
    )
    processo = forms.ModelChoiceField(
        queryset=ProcessoCompra.objects.filter(ativo=True)
    )
    subtipo = forms.ChoiceField(choices=ContratoCompra.SUBTIPO)

    def __init__(self, *args, **kwargs):
        objeto = ''
        num_pc = ''
        if 'processo_id' in kwargs:
            processo_id = kwargs.pop('processo_id')
            processo = Processo.objects.get(id=processo_id)
            objeto = processo.descricao
            num_pc = processo.processo_compra

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
        self.fields['subtipo'].widget.attrs.update(
            {'class': 'form-select'}
        )
        self.fields['fornecedor'].widget.attrs['readonly'] = True

        if objeto != "":
            self.fields['objeto'].initial = objeto

        if num_pc != "":
            self.fields['processo'].initial = num_pc

    class Meta:
        model = RevisaoContratoCompra
        fields = ['data_ini', 'data_fim', 'gestor', 'fiscal',
                  'data_assinatura', 'objeto', 'nome_simplificado']


class ContratoCompraEditForm(forms.ModelForm):
    numero_contrato = forms.CharField(max_length=19,
                                      label='Número',
                                      required=False)
    fornecedor = forms.ModelChoiceField(
        queryset=Pessoa.objects.filter(ativo=True, fornecedor=True)
    )
    processo = forms.ModelChoiceField(
        queryset=ProcessoCompra.objects.filter(ativo=True)
    )

    def __init__(self, *args, **kwargs):
        super(ContratoCompraEditForm, self).__init__(*args, **kwargs)
        contrato = kwargs.get('instance')
        numero = contrato.contrato.numero_formatado
        fornecedor = contrato.contrato.fornecedor
        processo = contrato.contrato.processo
        self.fields['numero_contrato'].initial = numero
        self.fields['fornecedor'].initial = fornecedor
        self.fields['processo'].initial = processo
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

    class Meta:
        model = RevisaoContratoCompra
        fields = ['data_ini', 'data_fim', 'gestor', 'fiscal',
                  'data_assinatura', 'objeto', 'nome_simplificado', 'subgrupo',
                  'area']
        widgets = {
            'subgrupo': autocomplete.ModelSelect2(
                url='subgrupo_autocomplete',
                attrs={
                    'class': 'form-control',
                    'data-minimum-input-length': 3,
                }
            )
        }


class RevisaContratoCompraForm(forms.ModelForm):
    numero_aditamento = forms.CharField(max_length=19,
                                        label='Número',
                                        required=False)

    def __init__(self, *args, **kwargs):
        contrato = kwargs.pop('contrato_id')
        super(RevisaContratoCompraForm, self).__init__(*args, **kwargs)
        self.fields['numero_aditamento'].widget.attrs.update(
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
        revisao_anterior = RevisaoContratoCompra.objects.get(
            contrato=contrato, is_vigente=True
        )
        self.fields['data_ini'].initial = revisao_anterior.data_ini
        self.fields['data_fim'].initial = revisao_anterior.data_fim
        self.fields['objeto'].initial = revisao_anterior.objeto

    class Meta:
        model = RevisaoContratoCompra
        fields = ['data_ini', 'data_fim', 'gestor', 'fiscal',
                  'data_assinatura', 'objeto', 'numero_aditamento']


class ItemContratoCompraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemContratoCompraForm, self).__init__(*args, **kwargs)
        self.fields['produto'].widget.attrs.update({'class': 'form-select'})
        self.fields['ord_item'].widget.attrs['readonly'] = True

    class Meta:
        model = ItemContratoCompra
        fields = ['ord_item', 'produto', 'descricao', 'quantidade',
                  'valor_unit', 'saldo_fis']


ItemContratoCompraFormset = forms.inlineformset_factory(
    RevisaoContratoCompra,
    ItemContratoCompra,
    form=ItemContratoCompraForm,
    extra=1, can_delete=True
)
