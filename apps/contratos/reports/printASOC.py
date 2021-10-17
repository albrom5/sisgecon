from django.http import HttpResponse

from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

from apps.contratos.models import RevisaoContratoCompra


def export_asoc_to_excel(request, pk):
    contrato = RevisaoContratoCompra.objects.get(id=pk)

    filepath = 'static\excel\ASEXCEL2021.xlsx'
    wb = load_workbook(filepath)
    sheet = wb.get_sheet_by_name('CNS_PrintAS')
    sheet['A2'] = contrato.contrato.numero_formatado
    sheet['B2'] = contrato.contrato.processo.processo_id.numero_sei
    sheet['C2'] = contrato.data_assinatura
    sheet['G2'] = contrato.contrato.fornecedor.nome
    wb.save(filepath)

    response = HttpResponse(content=save_virtual_workbook(wb),
                            content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename={contrato.numero_formatado}.xlsx'
    return response