#!/usr/bin/env python
# -*- coding: utf-8

from django.contrib import admin
from base.admin import DisplayableAdmin
from .models import Work, Tag


class WorkAdmin(DisplayableAdmin):
    pass


admin.site.register(Tag)
admin.site.register(Work, WorkAdmin)
