#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.template import (
    Library, Node, Variable, TemplateSyntaxError, TemplateDoesNotExist
)
from django.template.loader import get_template
from django.db.models import Q
from django.utils import six
from pages.models import Page

register = Library()


class SideBarNode(Node):
    def __init__(self, page, template_path):
        super(SideBarNode, self).__init__()
        self.page = page
        self.template_path = template_path

    def render(self, context):
        # Determine search criteria
        page = Variable(self.page).resolve(context)
        if isinstance(page, Page):
            pass
        else:
            if isinstance(page, six.string_types):
                lookup = Q(pk=page) | Q(slug=page)
            else:
                lookup = Q(pk=page)
            try:
                page = Page.objects.get(lookup)
            except Page.DoesNotExist:
                page = None

        if page is not None:
            root = page._root or page
            pages = Page.objects.public().filter(_root=root)
        else:
            pages = Page.objects.none()

        # Find template to use
        template_paths = [
            'pages/includes/{slug}_sidebar.html'.format(slug=page.slug),
            'pages/includes/sidebar.html'
        ]
        if self.template_path is not None:
            template_paths.insert(
                0, Variable(self.template_path).resolve(context)
            )

        for template_path in template_paths:
            try:
                template = get_template(template_path)
                break
            except TemplateDoesNotExist:
                pass

        context['pages'] = pages
        return template.render(context)


@register.tag
def sidebar(parser, token):
    """Renders the sidebar for a given page

    Usage: ``{% sidebar page template_path %}``

    A page's sidebar is based on its root parent's all decendants. ``page``
    can be a concrete pages.Page object, a string (the page's slug), any type
    matching the page's pk. ``template_path`` is optional, and defaults to
    ``pages/includes/{slug}_sidebar.html``, or ``pages/includes/sidebar.html``
    if the former does not exist.
    """
    tokens = token.split_contents()
    tag_name = tokens.pop(0)
    try:
        page = tokens.pop(0)
    except IndexError:
        raise TemplateSyntaxError(
            'Template tag {name} takes at least one argument.'.format(
                name=tag_name
            )
        )
    try:
        template_path = tokens.pop(0)
    except IndexError:
        template_path = None
    return SideBarNode(page, template_path)
