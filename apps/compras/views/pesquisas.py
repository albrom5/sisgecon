from django.shortcuts import render
from django.urls import reverse_lazy

from apps.processos.models import ProcessoCompra
from apps.compras.models import Pesquisa, ItemSC, ItemPesquisa
from apps.empresa.models import Funcionario

from apps.compras.forms import PesquisaForm


def nova_pesquisa_processo(request, processo_id):
    context = {}
    template_name = 'compras/nova_pesquisa_pc.html'

    processo = ProcessoCompra.objects.get(
        processo_id=processo_id)
    responsavel = Funcionario.objects.get(user=request.user)
    itens_processo = ItemSC.objects.filter(
        solicitacao__processo__processo_id=processo_id)

    if request.method == 'POST':
        form = PesquisaForm(request.POST)
        if form.is_valid():
            pesquisa = form.save(commit=False)
            pesquisa.processo = processo
            pesquisa.responsavel = responsavel
            pesquisa.save()
            for i, item in enumerate(itens_processo):
                ItemPesquisa.objects.create(pesquisa=pesquisa,
                                            produto=item.produto,
                                            quantidade=item.quantidade,
                                            ord_item=i)
            return reverse_lazy('edita_pesquisa',
                                kwargs={'pk': pesquisa.id})
    else:
        form = PesquisaForm()

    context['processo'] = processo
    context['form'] = form
    context['itens'] = itens_processo

    return render(request, template_name, context)


def edita_pesquisa(request, pk):
    return
