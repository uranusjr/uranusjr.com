#!/usr/bin/env python
# -*- coding: utf-8

from django.forms import widgets
from django.template import Context
from django.template.loader import get_template
from django.contrib.staticfiles.templatetags.staticfiles import static


class GhostdownWidget(widgets.Textarea):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        if 'class' not in attrs:
            attrs['class'] = 'entry-markdown-textarea'
        else:
            attrs['class'] = attrs['class'] + ' entry-markdown-textarea'
        return super(GhostdownWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        try:
            value = value.raw
        except AttributeError:
            pass
        textarea = super(GhostdownWidget, self).render(name, value, attrs)
        template = get_template('ghostdown/includes/editor.html')
        context = Context({'textarea': textarea})
        return template.render(context)

    class Media:
        css = {'all': (static('ghostdown/css/ghostdown.css'),)}
        js = (static('ghostdown/js/ghostdown.js'),)
