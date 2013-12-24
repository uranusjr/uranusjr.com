#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from base.admin import DisplayableAdmin
from .models import Page


class ExtraHeadersInline(DisplayableAdmin):
    model = Page.extra_header_paths.through


class PageAdmin(admin.ModelAdmin):

    list_display = ('title', 'short_description', 'state', 'published_at')
    list_editable = ('state', 'published_at')
    fieldsets = (
        (None, {'fields': (
            'title', 'short_description', 'image', 'content'
        )}),
        ('Publishing options', {'fields': ('state', 'published_at')}),
        ('Page options', {'fields': ('slug', 'parent')})
    )


admin.site.register(Page, PageAdmin)
