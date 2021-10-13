from django import forms

from dal import autocomplete

from .models import Produto

class ProdutoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['unidade'].widget.attrs.update({'class': 'form-select'})

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('descricao')
        qs = Produto.objects.filter(descricao=nome).exclude(
            descricao=self.instance.descricao)
        if qs:
            msg = "Já existe produto cadastrado com esse nome"
            self.add_error('descricao', msg)
        sigla = cleaned_data.get('sigla')
        qs = Produto.objects.filter(sigla=sigla).exclude(
            sigla=self.instance.sigla)
        if qs:
            msg = "Já existe produto cadastrado com essa sigla"
            self.add_error('sigla', msg)

    class Meta:
        model = Produto
        fields = ['descricao', 'unidade', 'sigla', 'subgrupo', 'especifica',
                  'numprotheus', 'tabela_eventos']
        widgets = {
            'subgrupo': autocomplete.ModelSelect2(
                url='subgrupo_autocomplete',
                attrs={'class': 'form-control',
                       'data-minimum-input-length': 3,
                       }
            )
        }