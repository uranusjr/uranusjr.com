#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import template
from django.utils.translation import ugettext as _
from base.models import ExtraPath

register = template.Library()


@register.inclusion_tag('base/includes/tabbar.html', takes_context=True)
def sidebar_tabs(context):
    request = context['request']

    def is_active(slug):
        return request.path.startswith('/{slug}'.format(slug=slug))

    TABS = (    # slug, name, is_active
        ('', _('about'), request.path == '/'),
        ('blog/', _('blog'), is_active('blog')),
        ('work/', _('work'), is_active('work')),
    )
    context['tabs'] = TABS
    return context


@register.inclusion_tag('base/includes/stylesheets.html')
def stylesheets(obj, link_type):
    files = ExtraPath.objects.filter(file_type='css', link_type=link_type)
    return {'files': files}


@register.inclusion_tag('base/includes/javascripts.html')
def javascripts(obj, link_type):
    files = ExtraPath.objects.filter(
        file_type='javascript', link_type=link_type
    )
    return {'files': files}
