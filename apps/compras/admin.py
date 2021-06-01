from django.contrib import admin
from .models.compras import ProcessoCompra, SolicitacaoCompra, ItemSC

admin.site.register(ProcessoCompra)
admin.site.register(SolicitacaoCompra)
admin.site.register(ItemSC)
