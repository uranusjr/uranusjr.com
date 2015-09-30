#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from .forms.widgets import PopupGhostdownInput
from .models import ExtraPath


def view_in_site(obj):
    html_format = '<a href="{url}" target="_blank">{text}</a>'
    return html_format.format(
        url=obj.get_absolute_url(), text=view_in_site.short_description,
    )

view_in_site.short_description = _('View in site')
view_in_site.allow_tags = True


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
        widgets = {'short_description': forms.Textarea}


class DisplayableAdmin(admin.ModelAdmin):

    form = DisplayableAdminForm
    inlines = (ExtraPathInline,)
