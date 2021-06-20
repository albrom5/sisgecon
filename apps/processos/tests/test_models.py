from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from apps.processos.models import ProcessoCompra, Processo


class ProcessoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Processo.objects.create(numero_sei='7210.2021/0001528-8',
                                descricao='Objeto teste 1',
                                tipo='PC',
                                data_autuacao='2021-06-30')
        Processo.objects.create(numero_sei='7210.2021/0001528-9',
                                descricao='Objeto teste 2',
                                tipo='PC',
                                data_autuacao='2021-06-30')

    def test_numero_sei_label(self):
        processo = Processo.objects.get(id=1)
        field_label = processo._meta.get_field('numero_sei').verbose_name
        self.assertEqual(field_label, 'Número SEI')

    def test_descricao_label(self):
        processo = Processo.objects.get(id=1)
        field_label = processo._meta.get_field('descricao').verbose_name
        self.assertEqual(field_label, 'Objeto')

    def test_data_autuacao_label(self):
        processo = Processo.objects.get(id=1)
        field_label = processo._meta.get_field('data_autuacao').verbose_name
        self.assertEqual(field_label, 'Autuado em:')


    def test_nome_esperado(self):
        processo = Processo.objects.get(id=1)
        nome_esperado = f'{processo.numero_sei} - {processo.descricao}'
        self.assertEqual(nome_esperado, str(processo))

    def test_validate_unique(self):
        numero_sei = '7210.2021/0001528-8'
        descricao = 'Objeto teste'
        tipo = 'PC'
        data_autuacao = '2021-06-30'
        processo = Processo(numero_sei=numero_sei,
                            descricao=descricao,
                            tipo=tipo,
                            data_autuacao=data_autuacao)
        try:
            processo.save()
        except ValidationError as e:
            self.assertEqual(e.message, 'Número de processo já cadastrado.')



