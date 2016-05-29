#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponsePermanentRedirect
from django.views.generic import ListView


class DisplayableListView(ListView):
    """Sensible implementation for all Displayable subclasses
    """
    template_name = 'displayable_list.html'
    context_object_name = 'obj_list'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        page_kwarg = self.page_kwarg
        if request.GET.get(page_kwarg) == '1':
            params = request.GET.copy()
            params.pop(page_kwarg)
            return HttpResponsePermanentRedirect(
                request.path + '?' + params.urlencode(),
            )
        return super(DisplayableListView, self).dispatch(
            request, *args, **kwargs
        )

    def get_title(self):
        return ''

    def get_context_data(self, **kwargs):
        context = super(DisplayableListView, self).get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context
