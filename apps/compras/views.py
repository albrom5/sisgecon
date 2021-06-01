from django.views.generic import CreateView
from .models.compras import ProcessoCompra


class ProcessoCompraNovo(CreateView):
    model = ProcessoCompra
