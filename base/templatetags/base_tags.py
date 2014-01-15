#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.http.request import QueryDict
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


@register.simple_tag(takes_context=True)
def absolute_uri(context, path):
    return context['request'].build_absolute_uri(path)


@register.inclusion_tag('base/includes/pagination.html', takes_context=True)
def pagination(context, page, page_key='page', max_link_count=9):
    if max_link_count < 1:
        raise TemplateSyntaxError(
            'Template tag pagination requires at least one link.'
        )
    page_range = page.paginator.page_range
    if len(page_range) > max_link_count:
        half_range = (max_link_count - 1) // 2
        start = max(page.number - half_range, 0)
        end = min(start + max_link_count, page.paginator.num_pages)
        page.visible_page_range = page_range[start:end]
    else:
        page.visible_page_range = page.paginator.page_range
    return {
        'querydict': context['request'].GET,
        'page': page,
        'page_key': page_key,
    }


class QueryStringNode(Node):
    def __init__(self, *args):
        self.args = args

    def render(self, context):
        if not len(self.args) or '=' in self.args[0]:
            querydict = QueryDict('', mutable=True)
        else:
            first = self.args[0]
            self.args = self.args[1:]
            querydict = Variable(first).resolve(context).copy()
        for pair in self.args:
            k, v = [Variable(p).resolve(context) for p in pair.split('=')]
            querydict[k] = v
        return querydict.urlencode()


@register.tag
def querystring(parser, token):
    tokens = token.split_contents()
    tokens.pop(0)   # tag_name
    return QueryStringNode(*tokens)


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
