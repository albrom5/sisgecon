from django import forms
from localflavor.br.forms import BRCNPJField, BRCPFField

from .models.empresas import PessoaJuridica, PessoaFisica, Contato


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
                  'estado', 'cep', 'insc_est', 'insc_mun']


class FornecedorPFForm(forms.ModelForm):
    cpf = BRCPFField(label='CPF')
    nome = forms.CharField(label='Nome')

    def __init__(self, *args, **kwargs):
        super(FornecedorPFForm, self).__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class': 'cpfmask'})
        self.fields['cep'].widget.attrs.update({'class': 'cep cepmask'})
        self.fields['logradouro'].widget.attrs.update({'class': 'rua'})
        self.fields['bairro'].widget.attrs.update({'class': 'bairro'})
        self.fields['cidade'].widget.attrs.update({'class': 'cidade'})
        self.fields['estado'].widget.attrs.update({'class': 'uf form-select'})

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf')
        qs = PessoaFisica.objects.filter(cpf=cpf).exclude(
            cpf=self.instance.cpf)
        if qs:
            msg = "Já existe fornecedor cadastrado com esse CPF"
            self.add_error('cpf', msg)

    class Meta:
        model = PessoaFisica
        fields = ['nome', 'cpf', 'logradouro',
                  'ender_num', 'ender_compl', 'bairro', 'cidade',
                  'estado', 'cep', 'rg', 'insc_mun']


class ContatoForm(forms.ModelForm):
    contato = forms.CharField(label='Número/Email')
    def __init__(self, *args, **kwargs):
        super(ContatoForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Contato
        fields = ['contato', 'tipo', 'responsavel', 'padrao']


ContatoFornFormset = forms.inlineformset_factory(PessoaJuridica, Contato,
                                                 form=ContatoForm, extra=1,
                                                 can_delete=True)

ContatoFornPFFormset = forms.inlineformset_factory(PessoaFisica, Contato,
                                                 form=ContatoForm, extra=1,
                                                 can_delete=True)
