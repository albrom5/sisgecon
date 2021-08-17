from django.db import models
from apps.base.models import BaseModel
from apps.empresa.models import Funcionario
from apps.produtos.models import Produto


class Briefing(BaseModel):
    numero = models.PositiveSmallIntegerField(null=True, blank=True)
    data_emissao = models.DateField(null=True, blank=True)


class RevisaoBriefing(BaseModel):
    briefing = models.ForeignKey(Briefing, on_delete=models.CASCADE)
    ordem = models.PositiveSmallIntegerField(null=True, blank=True)
    produtor = models.ForeignKey(Funcionario, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    observacoes = models.TextField(max_length=3000, null=True, blank=True)
    data_emissao = models.DateField(null=True, blank=True)
    is_vigente = models.BooleanField(default=True)

class ItemBriefing(BaseModel):
    revisao = models.ForeignKey(RevisaoBriefing, on_delete=models.CASCADE)
    ordem = models.PositiveSmallIntegerField(null=True, blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
