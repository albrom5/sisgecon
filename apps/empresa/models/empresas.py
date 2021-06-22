from django.db import models
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
