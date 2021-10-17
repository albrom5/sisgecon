from django.urls import path
from django.views.decorators.cache import never_cache

from .views import (ProcessoCompraNovo,
                    ProcessoCompraDetail,
                    ProcessoCompraEdit,
                    ProcessosCompraList)


urlpatterns = [
    path('', never_cache(ProcessosCompraList.as_view()),
         name='processos_list'),
    path('<int:pk>', never_cache(ProcessoCompraDetail.as_view()),
         name='processo_detail'),
    path('novo/', ProcessoCompraNovo.as_view(),
         name='processo_novo'),
    path('edit/<int:pk>', never_cache(ProcessoCompraEdit.as_view()),
         name='processo_edit'),
    ]
