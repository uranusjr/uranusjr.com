#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import template
from base.models import ExtraPath
from pages.models import Page

register = template.Library()


@register.inclusion_tag('base/includes/tabbar.html', takes_context=True)
def sidebar_tabs(context):
    request = context['request']

    def is_active(slug):
        return request.path.startswith('/{slug}'.format(slug=slug))

    root_pages = Page.objects.public().values(
        'slug', 'title'
    ).filter(parent=None).exclude(slug='index')

    # slug, name, is_active
    TABS = [{
        'slug': '',
        'title': Page.objects.get(slug='index').title,
        'is_active': (request.path == '/'),
    }]
    TABS += [{
        'slug': '{slug}/'.format(slug=p['slug']),
        'title': p['title'],
        'is_active': is_active(p['slug'])
    } for p in root_pages]
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
