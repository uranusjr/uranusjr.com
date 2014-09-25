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
        current_page = Variable(self.page).resolve(context)
        if isinstance(current_page, Page):
            page = current_page._root
        else:
            if isinstance(current_page, six.string_types):
                lookup = Q(slug=current_page)
            else:
                lookup = Q(pk=current_page)
            try:
                current_page = Page.objects.get(lookup)
            except Page.DoesNotExist:
                page = None
            else:
                page = current_page._root
        if page is None:
            page = current_page

        context['page'] = page      # This is what the sidebar is base on.

        # Find template to use with the folowing order:
        # 1. If the template tag is invoked with a specific path, try it.
        # 2. If there are templates named {page_slug}_sidebar.html, try it.
        # 3. sidebar.html, which should always exist.
        template_paths = ['pages/includes/sidebar.html']

        if page is not None:
            template_paths.append(
                'pages/includes/{slug}_sidebar.html'.format(slug=page.slug),
            )

        if self.template_path is not None:
            template_paths.append(
                Variable(self.template_path).resolve(context),
            )

        for template_path in reversed(template_paths):
            try:
                template = get_template(template_path)
                break
            except TemplateDoesNotExist:
                pass

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
