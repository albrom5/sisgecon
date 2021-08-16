from django.db import models

from apps.base.models import BaseModel
from apps.contratos.models import ContratoCompra
from apps.processos.models import Processo

class OrgaoSOF(BaseModel):
    cod = models.CharField(max_length=2)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class UnidadeSOF(BaseModel):
    cod = models.CharField(max_length=2)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class FuncaoSOF(BaseModel):
    cod = models.CharField(max_length=2)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class SubFuncaoSOF(BaseModel):
    cod = models.CharField(max_length=3)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class ProgramaSOF(BaseModel):
    cod = models.CharField(max_length=4)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class ProjetoAtividadeSOF(BaseModel):
    cod = models.CharField(max_length=4)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class CategoriaSOF(BaseModel):
    cod = models.CharField(max_length=1)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class GrupoSOF(BaseModel):
    cod = models.CharField(max_length=1)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class ModalidadeSOF(BaseModel):
    cod = models.CharField(max_length=2)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class ElementoSOF(BaseModel):
    cod = models.CharField(max_length=2)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class SubElementoSOF(BaseModel):
    cod = models.CharField(max_length=2)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class FonteRecursoSOF(BaseModel):
    cod = models.CharField(max_length=2)
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.cod} - {self.descricao}'


class Dotacao(BaseModel):
    orgao = models.ForeignKey(OrgaoSOF, on_delete=models.PROTECT)
    unidade = models.ForeignKey(UnidadeSOF, on_delete=models.PROTECT)
    funcao = models.ForeignKey(FuncaoSOF, on_delete=models.PROTECT)
    subfuncao = models.ForeignKey(SubFuncaoSOF, on_delete=models.PROTECT)
    programa = models.ForeignKey(ProgramaSOF, on_delete=models.PROTECT)
    projeto_atividade = models.ForeignKey(ProjetoAtividadeSOF,
                                          on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaSOF, on_delete=models.PROTECT)
    grupo = models.ForeignKey(GrupoSOF, on_delete=models.PROTECT)
    modalidade = models.ForeignKey(ModalidadeSOF, on_delete=models.PROTECT)
    elemento = models.ForeignKey(ElementoSOF, on_delete=models.PROTECT)
    subelemento = models.ForeignKey(SubElementoSOF, on_delete=models.PROTECT)
    fonte_recurso = models.ForeignKey(FonteRecursoSOF,
                                      on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.orgao.cod}.{self.unidade.cod}.{self.funcao.cod}.' \
               f'{self.subfuncao.cod}.{self.programa.cod}.' \
               f'{self.projeto_atividade.cod}.{self.categoria.cod}.' \
               f'{self.grupo.cod}.{self.modalidade.cod}.{self.elemento.cod}.' \
               f'{self.subelemento.cod}.{self.fonte_recurso.cod}'

    class Meta:
        verbose_name = 'Dotação Orçamentária'
        verbose_name_plural = "Dotações Orçamentárias"
        ordering = ['funcao', 'subfuncao']


class Reserva(BaseModel):
    numero = models.CharField(max_length=9)
    data_lancamento = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=19, decimal_places=6,
                                null=True, blank=True)
    dotacao = models.ForeignKey(Dotacao, on_delete=models.PROTECT)
    processo = models.ManyToManyField(Processo, blank=True)
    contrato_real = models.ManyToManyField(ContratoCompra, blank=True)

    def __str__(self):
        return f'SOF{self.numero}'


class ContratoSof(BaseModel):
    numero = models.CharField(max_length=9)
    data_lancamento = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=19, decimal_places=6,
                                null=True, blank=True)
    contrato_real = models.ForeignKey(ContratoCompra,
                                      on_delete=models.SET_NULL,
                                      null=True, blank=True)

    def __str__(self):
        return f'SOF{self.numero}'


class Empenho(BaseModel):
    numero = models.CharField(max_length=9)
    data_lancamento = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=19, decimal_places=6,
                                null=True, blank=True)
    dotacao = models.ForeignKey(Dotacao, on_delete=models.PROTECT)
    contrato_sof = models.ForeignKey(ContratoSof, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    contrato_real = models.ForeignKey(ContratoCompra,
                                      on_delete=models.SET_NULL,
                                      null=True, blank=True)

    def __str__(self):
        return f'SOF{self.numero}'

