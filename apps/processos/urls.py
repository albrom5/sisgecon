from django.urls import path
from .views import (ProcessoCompraNovo,
                    ProcessoCompraDetail,
                    ProcessoCompraEdit,
                    # processo_list)
                    ProcessosCompraList)


urlpatterns = [
    path('', ProcessosCompraList.as_view(),
         name='processos_list'),
    # path('', processo_list, name='processos_list'),
    path('<int:pk>', ProcessoCompraDetail.as_view(),
         name='processo_detail'),
    path('novo/', ProcessoCompraNovo.as_view(),
         name='processo_novo'),
    path('edit/<int:pk>', ProcessoCompraEdit.as_view(),
         name='processo_edit'),
    ]
