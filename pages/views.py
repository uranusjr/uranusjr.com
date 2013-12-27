#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.template.loader import find_template
from django.shortcuts import render
from .models import Page


def page(request, slug, template='pages/page.html'):
    try:
        page = Page.objects.published().get(slug=slug)
    except Page.DoesNotExist:
        raise Http404

    # Find the template to use by traversing the parenting chain. If nobody has
    # a custom template, use the default 'pages/page.html'
    parent = page
    while parent:
        template_candidate = 'pages/{slug}.html'.format(slug=parent.slug)
        try:
            find_template(template_candidate)
        except TemplateDoesNotExist:
            parent = parent.parent
        else:
            template = template_candidate
            break

    return render(request, template, {'page': page})
