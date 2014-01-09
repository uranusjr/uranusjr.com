#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.template import (
    Library, Context, Node, Variable, TemplateSyntaxError
)
from django.template.loader import get_template
from base.models import ExtraPath
from pages.models import Page

register = Library()


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


@register.inclusion_tag('base/includes/disqus.html')
def disqus(unique_id):
    return {'unique_id': unique_id}


class ExtraPathNode(Node):
    def __init__(self, file_type, link_type, obj, template_name):
        self.file_type = file_type
        self.link_type = link_type
        self.obj = obj
        self.template_name = template_name

    def render(self, context):
        owner = Variable(self.obj).resolve(context)
        files = ExtraPath.objects.filter(
            owner_id=owner.pk, file_type=self.file_type,
            link_type=self.link_type,
        )
        template = get_template(self.template_name)
        return template.render(Context({'files': files}))


def _parse_extra_path(token):
    tokens = token.split_contents()
    tag_name = tokens.pop(0)
    if len(tokens) != 2:
        raise TemplateSyntaxError(
            'Template tag {name} takes exactly two arguments.'.format(
                name=tag_name
            )
        )
    link_types = {
        'header': ExtraPath.LINK_TYPE_HEADER,
        'footer': ExtraPath.LINK_TYPE_FOOTER,
    }
    try:
        key = tokens.pop(0).lower()
        link_type = link_types[key]
    except KeyError:
        raise TemplateSyntaxError(
            'First argument of template tag {name} should not be {key}, but '
            'one of the followings: {candidates}.'.format(
                name=tag_name, key=key,
                candidates=', '.join(link_types.keys()),
            )
        )
    return tokens[0], link_type


@register.tag
def stylesheets(parser, token):
    obj, link_type = _parse_extra_path(token)
    return ExtraPathNode(
        'css', link_type, obj, 'base/includes/stylesheets.html'
    )


@register.tag
def javascripts(parser, token):
    obj, link_type = _parse_extra_path(token)
    return ExtraPathNode(
        'javascript', link_type, obj, 'base/includes/javascripts.html'
    )
