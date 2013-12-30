#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from base.admin import DisplayableAdmin, DisplayableAdminForm
from .models import Page


def _page_parent_link(obj):
    parent = obj.parent
    if parent is None:
        return _('--')
    return '<a href="{url}">{title}</a>'.format(
        url=parent.get_absolute_url(),
        title=parent.title
    )

_page_parent_link.short_description = _('parent')
_page_parent_link.allow_tags = True


class PageAdminForm(DisplayableAdminForm):
    class Meta:
        widgets = {
            'image_caption': forms.Textarea
        }


class PageAdmin(DisplayableAdmin):

    form = PageAdminForm
    list_display = (
        'title', 'short_description', 'state', 'published_at',
        _page_parent_link, 'order'
    )
    list_editable = ('state', 'published_at', 'order')
    fieldsets = (
        (None, {'fields': (
            'title', 'short_description', 'image', 'image_caption', 'content'
        )}),
        ('Publishing options', {'fields': ('state', 'published_at')}),
        ('Page options', {'fields': ('slug', 'parent', 'order')})
    )


admin.site.register(Page, PageAdmin)
