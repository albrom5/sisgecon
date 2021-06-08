from django.urls import path

from apps.compras.views import SolitacaoCompraNova

urlpatterns = [
    path('<int:processo_id>/nova/', SolitacaoCompraNova.as_view(), name='sc_nova')
]
