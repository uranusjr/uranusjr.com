#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from base.views import DisplayableListView
from .models import Talk


class TalkListView(DisplayableListView):

    template_name = 'talk_list.html'

    def get_queryset(self):
        talks = Talk.objects.published()
        return talks.order_by('-published_at', '-pk')

    def get_title(self):
        return _('Recent talks')


talk_list = TalkListView.as_view()
