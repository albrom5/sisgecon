from django.db import models
from .base import BaseModel


class Status(BaseModel):
    TIPO_STATUS = [('LC', 'Licitação'),
                   ('PC', 'Processo de Compra'),
                   ('CC', 'Contrato de Compra')]
    tipo = models.CharField(max_length=2, null=True, blank=True,
                            choices=TIPO_STATUS)
    descricao = models.CharField(max_length=30)
    contabiliza_saldo = models.BooleanField(default=True)

    def __str__(self):
        return self.descricao
