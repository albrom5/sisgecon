from django.contrib import admin
from .models.compras import SolicitacaoCompra, ItemSC


admin.site.register(SolicitacaoCompra)
admin.site.register(ItemSC)
