
import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('apps.base.urls')),
    path('produtos/', include('apps.produtos.urls')),
    path('processos/', include('apps.processos.urls')),
    path('compras/', include('apps.compras.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
