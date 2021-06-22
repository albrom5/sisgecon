from django.db import models
from apps.base.models import BaseModel


class Diretoria(BaseModel):
    sigla = models.CharField(max_length=5, unique=True)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.sigla


class Gerencia(BaseModel):
    sigla = models.CharField(max_length=5, unique=True)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.sigla


class Coordenadoria(BaseModel):
    sigla = models.CharField(max_length=5, unique=True)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.sigla


class Departamento(BaseModel):
    diretoria = models.ForeignKey(Diretoria, on_delete=models.SET_NULL,
                                  blank=True, null=True,
                                  limit_choices_to={'ativo': True})
    gerencia = models.ForeignKey(Gerencia, on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 limit_choices_to={'ativo': True})
    coordenadoria = models.ForeignKey(Coordenadoria, on_delete=models.SET_NULL,
                                      blank=True, null=True,
                                      limit_choices_to={'ativo': True})

    def __str__(self):
        if self.diretoria and self.gerencia and self.coordenadoria:
            return f'{self.diretoria}/{self.gerencia}/{self.coordenadoria} - {self.coordenadoria.nome}'
        elif self.diretoria and self.gerencia:
            return f'{self.diretoria}/{self.gerencia} - {self.gerencia.nome}'
        elif self.diretoria:
            return f'{self.diretoria} - {self.diretoria.nome}'

    class Meta:
        ordering = ['diretoria', 'gerencia', 'coordenadoria']
