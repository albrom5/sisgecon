from django.db import models
from django.contrib.auth.models import User
from apps.base.models import BaseModel
from .departamentos import Departamento


class Cargo(BaseModel):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Funcionario(BaseModel):
    user = models.OneToOneField(User, primary_key=True,
                                on_delete=models.PROTECT)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL,
                                     blank=True, null=True,
                                     limit_choices_to={'ativo': True})
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL,
                              blank=True, null=True,
                              limit_choices_to={'ativo': True})

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
