from dal import autocomplete

from django.db.models import Q

from apps.empresa.models import (
    Departamento, Funcionario, CentroCusto, ContaContabil
)

from apps.produtos.models import Produto


class AreaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Departamento.objects.filter(ativo=True)
        if self.q:
            qs = qs.filter(
                Q(diretoria__sigla__istartswith=self.q) |
                Q(gerencia__sigla__istartswith=self.q) |
                Q(coordenadoria__sigla__istartswith=self.q)
            )
        return qs


class ResponsavelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Funcionario.objects.filter(ativo=True)
        if self.q:
            qs = qs.filter(
                Q(user__first_name__icontains=self.q) |
                Q(user__last_name__icontains=self.q)
                )
        return qs


class CentroCustoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CentroCusto.objects.filter(ativo=True)
        if self.q:
            qs = qs.filter(codigo__istartswith=self.q)
        return qs


class ContaContabilAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ContaContabil.objects.filter(ativo=True)
        if self.q:
            qs = qs.filter(codigo__istartswith=self.q)
        return qs


class ProdutoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Produto.objects.filter(ativo=True)
        if self.q:
            qs = qs.filter(Q(descricao__icontains=self.q) |
                           Q(numprotheus__icontains=self.q)
                           )
        return qs
