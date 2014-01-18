#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import ListView


class DisplayableListView(ListView):
    """Sensible implementation for all Displayable subclasses
    """
    template_name = 'displayable_list.html'
    context_object_name = 'obj_list'
    paginate_by = 10

    def get_title(self):
        return ''

    def get_context_data(self, **kwargs):
        context = super(DisplayableListView, self).get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context
