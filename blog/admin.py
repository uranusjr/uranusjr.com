#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin
from base.admin import DisplayableAdmin, TagAdmin, ElementAdmin, view_in_site
from .models import Post, Category, Tag


class PostAdmin(DisplayableAdmin):

    list_display = (
        'title', 'short_description', 'state', 'published_at', view_in_site
    )
    list_editable = ('state', 'published_at')
    fieldsets = (
        (None, {'fields': (
            ('title', 'category'), 'short_description', 'content',
        )}),
        ('Page options', {
            'fields': ('slug', 'state', 'published_at'),
            'classes': ('grp-collapse', 'grp-open'),
        }),
        ('Tags', {
            'fields': ('tags',),
            'classes': ('grp-collapse', 'grp-closed'),
        }),
    )
    filter_horizontal = ('tags',)
    ordering = ('-published_at',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, ElementAdmin)
admin.site.register(Post, PostAdmin)
