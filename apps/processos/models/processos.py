from django.db import models
from apps.base.models import Status, BaseModel


class Modalidade(BaseModel):
    sigla = models.CharField(max_length=20)
    fundamento = models.CharField(max_length=50)

    def __str__(self):
        return self.sigla


class Sistema(BaseModel):
    descricao = models.CharField(max_length=15)

    def __str__(self):
        return self.descricao


class Processo(BaseModel):
    TIPO_PROCESSO = [('PC', 'Processo de Compra')]
    numero_sei = models.CharField(verbose_name='Número SEI', max_length=19,
                                  unique=True)
    tipo = models.CharField(max_length=2, choices=TIPO_PROCESSO)
    descricao = models.CharField(max_length=250, null=True, blank=True)
    data_autuacao = models.DateField(verbose_name='Autuado em:', null=True,
                                     blank=True)

    def __str__(self):
        return f'{self.numero_sei} - {self.descricao}'


class ProcessoCompra(BaseModel):
    processo_id = models.OneToOneField(Processo, on_delete=models.PROTECT,
                                       primary_key=True,
                                       related_name='processo_compra')
    modalidade = models.ForeignKey(Modalidade, on_delete=models.PROTECT,
                                   null=True, blank=True,
                                   limit_choices_to={'ativo': True})
    numero_edital = models.CharField(max_length=12, null=True, blank=True)
    sistema = models.ForeignKey(Sistema, on_delete=models.SET_NULL, null=True,
                                blank=True, limit_choices_to={'ativo': True})
    refer_sistema = models.CharField(
        verbose_name='Número de Referência no Sistema', max_length=15,
        null=True, blank=True)
    data_gco = models.DateField(verbose_name='Recebido na GCO em:', null=True,
                                blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True,
                               blank=True, limit_choices_to={'tipo': 'PC',
                                                             'ativo': True})

# TODO Criar campos responsável, área (com relacionamentos)

    def __str__(self):
        return f'{self.processo_id.numero_sei} - {self.processo_id.descricao}'

    class Meta:
        ordering = ['-data_gco']