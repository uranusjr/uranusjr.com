#!/usr/bin/env python
# -*- coding: utf-8

from django import forms
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from .models import ExtraPath


class ExtraPathInline(GenericTabularInline):
    model = ExtraPath
    ct_field = 'owner_type'
    ct_fk_field = 'owner_id'
    extra = 0


class DisplayableAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'short_description': forms.Textarea
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
