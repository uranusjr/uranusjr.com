#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'state', 'published_at')
    list_editable = ('state', 'published_at')


admin.site.register(Page, PageAdmin)
