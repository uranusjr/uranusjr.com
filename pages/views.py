#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render
from .models import Page


def page(request, slug, template='pages/page.html'):
    try:
        page = Page.objects.published().get(slug=slug)
    except Page.DoesNotExist:
        raise Http404
    parent = page
    templates = []
    while parent:
        templates.append('pages/{slug}.html'.format(slug=parent.slug))
        parent = parent.parent
    templates.append(template)
    return render(request, templates, {'page': page})
