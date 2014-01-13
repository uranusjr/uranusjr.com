#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.contrib import admin
from base.admin import DisplayableAdmin, TagAdmin, ElementAdmin
from .models import Work, Tag, Category


class WorkAdmin(DisplayableAdmin):
    list_display = (
        'title', 'short_description', 'state', 'published_at',
        'work_type', 'order'
    )
    list_editable = ('state', 'published_at', 'work_type', 'order')
    fieldsets = (
        (None, {'fields': (
            ('title', 'category'), 'short_description', 'work_type',
        )}),
        ('Content', {
            'fields': ('url', 'content'),
            'classes': ('grp-collapse', 'grp-open'),
        }),
        ('Publishing options', {
            'fields': ('slug', 'state', 'published_at'),
            'classes': ('grp-collapse', 'grp-open'),
        }),
        ('Optional', {
            'fields': ('tags', 'image'),
            'classes': ('grp-collapse', 'grp-closed'),
        }),
    )
    filter_horizontal = ('tags',)


admin.site.register(Category, ElementAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Work, WorkAdmin)
