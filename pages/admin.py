#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from base.admin import DisplayableAdmin, DisplayableAdminForm, view_in_site
from .models import Page


def _page_parent_admin_link(obj):
    parent = obj.parent
    if parent is None:
        return _('--')
    return '<a href="{url}">{title}</a>'.format(
        url=reverse('admin:pages_page_change', args=(parent.id,)),
        title=parent.title,
    )

_page_parent_admin_link.short_description = _('parent')
_page_parent_admin_link.allow_tags = True


class PageAdminForm(DisplayableAdminForm):
    def __init__(self, *args, **kwargs):
        super(PageAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            queryset = Page.objects.exclude(pk=self.instance.pk).exclude(
                pk__in=self.instance.descendants.all()
            )
            self.fields['parent'].queryset = queryset


class PageAdmin(DisplayableAdmin):

    list_display = (
        'title', 'short_description', 'state', 'published_at',
        _page_parent_admin_link, 'order', view_in_site
    )
    list_editable = ('state', 'published_at', 'order')
    fieldsets = (
        (None, {'fields': (
            'title', 'short_description', 'image', 'image_caption',
        )}),
        ('Publishing options', {'fields': ('state', 'published_at')}),
        ('Page options', {'fields': ('slug', 'parent', 'order')})
    )
    form = PageAdminForm


admin.site.register(Page, PageAdmin)
