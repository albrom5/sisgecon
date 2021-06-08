from django.views.generic import ListView, CreateView, DetailView, UpdateView

from apps.base.views_mixins import (
    CheckPermissionMixin
)


class CustomListView(CheckPermissionMixin, ListView):

    def __init__(self, *args, **kwargs):
        super(CustomListView, self).__init__(*args, **kwargs)

    def get_paginate_by(self, queryset):
        """
        Try to fetch pagination by user settings,
        If there is none fallback to the original.
        """
        pagina = self.request.GET.get('page_size')
        if pagina:
            self.paginate_by = pagina
        return self.paginate_by


class CustomCreateView(CheckPermissionMixin, CreateView):

    def __init__(self, *args, **kwargs):
        super(CustomCreateView, self).__init__(*args, **kwargs)


class CustomDetailView(CheckPermissionMixin, DetailView):

    def __init__(self, *args, **kwargs):
        super(CustomDetailView, self).__init__(*args, **kwargs)


class CustomUpdateView(CheckPermissionMixin, UpdateView):

    def __init__(self, *args, **kwargs):
        super(CustomUpdateView, self).__init__(*args, **kwargs)
