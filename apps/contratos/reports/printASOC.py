import os
from sisgecon.settings import BASE_DIR

from django.http import HttpResponse

from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

from apps.compras.models import SolicitacaoCompra
from apps.contratos.models import RevisaoContratoCompra, ItemContratoCompra
from apps.empresa.models import PessoaJuridica, PessoaFisica, Contato


def export_asoc_to_excel(request, pk):
    contrato = RevisaoContratoCompra.objects.get(id=pk)
    scs = SolicitacaoCompra.objects.filter(processo=contrato.contrato.processo)
    lista_scs = []
    for sc in scs:
        sc_dict = {
            'numsc': sc.numsc,
            'area': sc.area,
            'ccusto': sc.centro_custo
        }
        lista_scs.append(sc_dict)

    numsc = [sc['numsc'] for sc in lista_scs]
    areas = [str(sc['area']) for sc in lista_scs]
    ccustos = [str(sc['ccusto']) for sc in lista_scs]

    contatos = Contato.objects.filter(pessoa=contrato.contrato.fornecedor)
    telefones = []
    emails = []
    responsaveis = []

    for contato in contatos:
        if contato.tipo == 'Telefone':
            telefones.append(contato.contato)
        elif contato.tipo == 'Email':
            emails.append(contato.contato)

        if contato.responsavel:
            responsaveis.append(contato.responsavel)

    if contrato.contrato.fornecedor.tipo == 'PJ':
        fornecedor = PessoaJuridica.objects.get(
            id=contrato.contrato.fornecedor_id
        )
        cnpj_cpf = fornecedor.cnpj
        ie_rg = fornecedor.insc_est
    else:
        fornecedor = PessoaFisica.objects.get(
            id=contrato.contrato.fornecedor_id
        )
        cnpj_cpf = fornecedor.cpf
        ie_rg = fornecedor.rg

    itens_contrato = ItemContratoCompra.objects.filter(revisao=contrato)

    lista_itens = []
    for item in itens_contrato:
        item_dict = {
            'ordem': item.ord_item,
            'produto': item.produto.descricao,
            'descricao_completa': item.descricao,
            'quantidade': item.quantidade,
            'valor_unit': item.valor_unit,
            'unidade': item.produto.unidade.descricao
        }
        lista_itens.append(item_dict)



    filepath = os.path.join(BASE_DIR, 'static\excel\ASEXCEL2021.xlsx')
    # filepath = '/home/alberto/projetos/django/sisgecon/sisgecon/static/excel/ASEXCEL2021.xlsx'
    wb = load_workbook(filepath)
    sheet = wb.get_sheet_by_name('dados')
    sheet['B3'] = str(contrato.contrato.get_subtipo_display()).upper()
    sheet['B4'] = contrato.contrato.numero_formatado
    sheet['B8'] = contrato.contrato.processo.processo_id.numero_sei
    sheet['B5'] = contrato.data_assinatura
    sheet['B7'] = contrato.contrato.modalidade.fundamento
    sheet['B9'] = ', '.join(numsc)
    sheet['B10'] = ', '.join(set(areas))
    sheet['B26'] = contrato.contrato.fornecedor.nome
    sheet['B27'] = contrato.contrato.fornecedor.endereco_completo
    sheet['B29'] = contrato.contrato.fornecedor.estado
    sheet['B28'] = contrato.contrato.fornecedor.cidade
    sheet['B31'] = cnpj_cpf
    sheet['B32'] = ie_rg
    sheet['B30'] = contrato.contrato.fornecedor.cep
    sheet['B33'] = contrato.contrato.fornecedor.insc_mun
    sheet['B34'] = ', '.join(telefones)
    sheet['B35'] = ', '.join(emails)
    sheet['B36'] = ', '.join(set(responsaveis))
    sheet['B38'] = contrato.objeto
    sheet['B15'] = ', '.join(set(ccustos))
    sheet['B41'] = contrato.valor_total

    for indice, item in enumerate(lista_itens):
        linha = str(indice + 2)
        sheet['M' + linha] = item['ordem']
        sheet['N' + linha] = item['produto']
        sheet['O' + linha] = item['descricao_completa']
        sheet['P' + linha] = item['quantidade']
        sheet['Q' + linha] = item['valor_unit']
        sheet['R' + linha] = item['unidade']

    # wb.save(filepath)

    response = HttpResponse(content=save_virtual_workbook(wb),
                            content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename={contrato.contrato.numero_formatado}.xlsx'
    return response
