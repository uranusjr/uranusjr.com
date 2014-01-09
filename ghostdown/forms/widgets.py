#!/usr/bin/env python
# -*- coding: utf-8

from django.forms import widgets
from django.template import Context
from django.template.loader import get_template


class GhostdownWidget(widgets.HiddenInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        if 'class' not in attrs:
            attrs['class'] = 'entry-markdown-input'
        else:
            attrs['class'] = attrs['class'] + ' entry-markdown-input'
        return super(GhostdownWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        try:
            value = value.raw
        except AttributeError:
            pass
        original = super(GhostdownWidget, self).render(name, value, attrs)
        template = get_template('ghostdown/includes/editor.html')
        context = Context({
            'original': original, 'content': value
        })
        return template.render(context)

    class Media:
        css = {'all': ('ghostdown/css/ghostdown.css',)}
        js = ('ghostdown/js/ghostdown.js',)
