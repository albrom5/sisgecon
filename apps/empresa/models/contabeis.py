from django.db import models
from apps.base.models import BaseModel
from apps.empresa.models import Departamento


class CentroCusto(BaseModel):
    codigo = models.CharField(max_length=10)
    descricao = models.CharField(max_length=300)
    area = models.ManyToManyField(Departamento)

    def __str__(self):
        return f'{self.codigo} - {self.descricao}'

    class Meta:
        verbose_name = "Centro de Custo"
        verbose_name_plural = "Centros de Custo"
        ordering = ['codigo', 'descricao']


class ContaContabil(BaseModel):
    codigo = models.CharField(max_length=10)
    descricao = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.codigo} - {self.descricao}'

    class Meta:
        verbose_name = "Conta Contábil"
        verbose_name_plural = "Contas Contábeis"
        ordering = ['codigo', 'descricao']
