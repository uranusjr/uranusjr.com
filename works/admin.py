#!/usr/bin/env python
# -*- coding: utf-8

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
            ('title', 'category'), 'short_description', 'tags', 'image',
            'content',
        )}),
        ('Publishing options', {'fields': ('state', 'published_at')}),
        ('Page options', {'fields': ('slug', 'order')})
    )
    filter_horizontal = ('tags',)


admin.site.register(Category, ElementAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Work, WorkAdmin)
