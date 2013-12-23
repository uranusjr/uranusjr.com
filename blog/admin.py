#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'short_description', 'state', 'published_at')
    list_editable = ('state', 'published_at')
    fieldsets = (
        (None, {'fields': (
            ('title', 'category'), 'short_description', 'tags', 'content'
        )}),
        ('Publishing options', {'fields': ('state', 'published_at')}),
        ('Page options', {'fields': ('slug',)})
    )
    filter_horizontal = ('tags',)

    class Media:
        css = {
            'all': ('base/css/markitup.css',)
        }
        js = (
            'filebrowser/js/AddFileBrowser.js',
        )

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
