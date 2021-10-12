from django.db import models

from apps.base.models import BaseModel
from apps.contratos.models import RevisaoContratoVenda


class Evento(BaseModel):
    contrato = models.ForeignKey(RevisaoContratoVenda,
                                 on_delete=models.PROTECT)
    descricao = models.CharField(max_length=500)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.descricao


class SubEvento(BaseModel):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=500)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.evento.descricao} - {self.descricao}'
