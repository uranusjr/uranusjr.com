#!/usr/bin/env python
# -*- coding: utf-8

from django.contrib import admin


class DisplayableAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('base/css/markitup.css',)
        }
        js = (
            'filebrowser/js/AddFileBrowser.js',
        )
