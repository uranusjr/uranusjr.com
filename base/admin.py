#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from ghostdown.forms.widgets import GhostdownWidget
from .models import ExtraPath


class ExtraPathInline(GenericTabularInline):
    model = ExtraPath
    ct_field = 'owner_type'
    ct_fk_field = 'owner_id'
    extra = 0
    classes = ('grp-collapse', 'grp-closed')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class ElementAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


class DisplayableAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'short_description': forms.Textarea,
            'content': GhostdownWidget,
        }


class DisplayableAdmin(admin.ModelAdmin):

    form = DisplayableAdminForm
    inlines = (ExtraPathInline,)

    class Media:
        css = {
            'all': ('base/css/markitup.css',)
        }
        js = (
            'filebrowser/js/AddFileBrowser.js',
        )
