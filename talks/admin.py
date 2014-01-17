#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from base.admin import DisplayableAdmin, TagAdmin
from .models import Tag, Talk


class TalkAdmin(DisplayableAdmin):
    list_display = (
        'title', 'short_description', 'state', 'published_at',
    )
    list_editable = ('state', 'published_at')
    fieldsets = (
        (None, {'fields': (
            'title', 'short_description', 'url', 'tags'
        )}),
        ('Page options', {
            'fields': ('slug', 'state', 'published_at'),
            'classes': ('grp-collapse', 'grp-open'),
        }),
    )
    filter_horizontal = ('tags',)
    ordering = ('-published_at',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Talk, TalkAdmin)
