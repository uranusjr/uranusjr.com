#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import Http404
from django.utils.translation import ugettext as _
from base.views import DisplayableListView
from .models import Talk, Tag


class TalkListView(DisplayableListView):

    template_name = 'talk_list.html'

    def get_queryset(self):
        talks = Talk.objects.published()
        return talks.order_by('-published_at', '-pk')

    def get_title(self):
        return _('Recent talks')


class TagTalkListView(TalkListView):
    def get(self, request, *args, **kwargs):
        try:
            self.tag = Tag.objects.get(slug=kwargs['slug'])
        except Tag.DoesNotExist:
            raise Http404
        return super(TagTalkListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        talks = super(TagTalkListView, self).get_queryset()
        return talks.filter(tags=self.tag)

    def get_title(self):
        title_format = _('Talks with tag “{name}”')
        return title_format.format(name=self.tag.name)


talk_list = TalkListView.as_view()
tag = TagTalkListView.as_view()
