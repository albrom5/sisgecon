from django.core.exceptions import ValidationError
from django.db import models
from apps.base.models import Status, BaseModel
from apps.produtos.models import SubGrupoProduto
from apps.empresa.models import Departamento, Funcionario


class Modalidade(BaseModel):
    sigla = models.CharField(max_length=30)
    fundamento = models.CharField(max_length=150)

    def __str__(self):
        return self.sigla


class Sistema(BaseModel):
    descricao = models.CharField(max_length=30)

    def __str__(self):
        return self.descricao


class Processo(BaseModel):
    TIPO_PROCESSO = [('PC', 'Processo de Compra')]
    numero_sei = models.CharField(verbose_name='Número SEI', max_length=19,
                                  unique=True)
    tipo = models.CharField(max_length=2, choices=TIPO_PROCESSO)
    descricao = models.CharField(verbose_name='Objeto', max_length=500,
                                 null=True, blank=True)
    data_autuacao = models.DateField(verbose_name='Autuado em:', null=True,
                                     blank=True)
    # TODO Testar exclude self.pk no filtro

    def validate_unique(self, exclude=None):
        qs = Processo.objects.filter(numero_sei=self.numero_sei).exclude(
            id=self.id
        )
        if qs:
            raise ValidationError('Número de processo já cadastrado.')

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Processo, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero_sei} - {self.descricao}'


class ProcessoCompra(BaseModel):
    processo_id = models.OneToOneField(Processo, on_delete=models.PROTECT,
                                       primary_key=True,
                                       related_name='processo_compra')
    modalidade = models.ForeignKey(Modalidade, on_delete=models.PROTECT,
                                   null=True, blank=True,
                                   limit_choices_to={'ativo': True})
    sistema = models.ForeignKey(Sistema, on_delete=models.SET_NULL, null=True,
                                blank=True, limit_choices_to={'ativo': True})
    data_gco = models.DateField(verbose_name='Recebido na GCO em:', null=True,
                                blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True,
                               blank=True, limit_choices_to={'tipo': 'PC',
                                                             'ativo': True})
    subgrupo = models.ForeignKey(SubGrupoProduto, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    area = models.ManyToManyField(Departamento)
    comprador = models.ForeignKey(Funcionario, on_delete=models.SET_NULL,
                                  null=True, blank=True)

    def __str__(self):
        return f'{self.processo_id.numero_sei} - {self.processo_id.descricao}'

    class Meta:
        ordering = ['-data_gco']
