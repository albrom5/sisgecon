from dal import autocomplete

from django.db.models import Q

from .models import SubGrupoProduto

class SubgrupoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SubGrupoProduto.objects.filter(ativo=True)
        if self.q:
            qs = qs.filter(
                Q(descricao__icontains=self.q) |
                Q(grupo__descricao__icontains=self.q) |
                Q(classe__descricao__icontains=self.q))
        return qs
