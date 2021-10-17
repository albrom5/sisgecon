from django.db import models
from localflavor.br.models import BRStateField

from apps.base.models import BaseModel


class Pessoa(BaseModel):
    TIPO_PESSOA = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica')
    ]
    tipo = models.CharField(max_length=2, choices=TIPO_PESSOA)
    nome = models.CharField(max_length=300)
    insc_mun = models.CharField(verbose_name='Inscrição Municipal',
                                max_length=30, null=True, blank=True)
    cliente = models.BooleanField(default=False)
    fornecedor = models.BooleanField(default=False)
    logradouro = models.CharField(verbose_name='Endereço',
                                  max_length=300, null=True, blank=True)
    ender_num = models.CharField(verbose_name='Número',
                                 max_length=30, null=True, blank=True)
    ender_compl = models.CharField(verbose_name='Complemento',
                                   max_length=50, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = BRStateField(null=True, blank=True)
    pais = models.CharField(max_length=100, default='Brasil')
    cep = models.CharField(verbose_name='CEP', max_length=9,
                           null=True, blank=True)

    @property
    def endereco_completo(self):
        return f'{self.logradouro}, {self.ender_num} {self.ender_compl} - ' \
               f'{self.bairro}'

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        ordering = ['nome']


class PessoaJuridica(Pessoa):
    cnpj = models.CharField(max_length=18, unique=True)
    insc_est = models.CharField(verbose_name='Inscrição Estadual',
                                max_length=30, null=True, blank=True)
    nome_fantasia = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.cnpj} - {self.nome}'


class PessoaFisica(Pessoa):
    cpf = models.CharField(max_length=18, unique=True)
    rg = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.cpf} - {self.nome}'


class Contato(BaseModel):
    TIPO_CONTATO = [
        ('Email', 'Email'),
        ('Telefone', 'Telefone')
    ]
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE,
                               related_name='contatos')
    tipo = models.CharField(max_length=8, choices=TIPO_CONTATO)
    contato = models.CharField(max_length=50)
    responsavel = models.CharField(max_length=100, null=True, blank=True)
    padrao = models.BooleanField(default=True)
