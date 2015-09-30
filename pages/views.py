#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

from .models import Page


def page(request, slug, template='pages/page.html'):
    index_path = reverse('pages:index')
    if slug == 'index' and request.path != index_path:
        return redirect(index_path)
    try:
        page = Page.objects.published().get(slug=slug)
    except Page.DoesNotExist:
        raise Http404

    custom_template = 'pages/{slug}.html'.format(slug=page.slug)
    try:
        get_template(custom_template)
    except TemplateDoesNotExist:
        pass
    else:
        template = custom_template

    return render(request, template, {'page': page})
