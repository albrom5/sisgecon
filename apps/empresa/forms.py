from django import forms
from localflavor.br.forms import BRCNPJField

from .models.empresas import PessoaJuridica, Contato


class FornecedorPJForm(forms.ModelForm):
    cnpj = BRCNPJField(label='CNPJ')
    nome = forms.CharField(label='Razão Social')

    def __init__(self, *args, **kwargs):
        super(FornecedorPJForm, self).__init__(*args, **kwargs)
        self.fields['cnpj'].widget.attrs.update({'class': 'cnpjmask'})
        self.fields['cep'].widget.attrs.update({'class': 'cep cepmask'})
        self.fields['logradouro'].widget.attrs.update({'class': 'rua'})
        self.fields['bairro'].widget.attrs.update({'class': 'bairro'})
        self.fields['cidade'].widget.attrs.update({'class': 'cidade'})
        self.fields['estado'].widget.attrs.update({'class': 'uf form-select'})

    def clean(self):
        cleaned_data = super().clean()
        cnpj = cleaned_data.get('cnpj')
        qs = PessoaJuridica.objects.filter(cnpj=cnpj).exclude(
            cnpj=self.instance.cnpj)
        if qs:
            msg = "Já existe fornecedor cadastrado com esse CNPJ"
            self.add_error('cnpj', msg)

    class Meta:
        model = PessoaJuridica
        fields = ['nome', 'cnpj', 'nome_fantasia', 'logradouro',
                  'ender_num', 'ender_compl', 'bairro', 'cidade',
                  'estado', 'cep']


class ContatoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContatoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contato
        fields = ['contato', 'tipo', 'responsavel', 'padrao']


ContatoFornFormset = forms.inlineformset_factory(PessoaJuridica, Contato,
                                                 form=ContatoForm, extra=1,
                                                 can_delete=True)
