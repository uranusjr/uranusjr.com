#!/usr/bin/env python
# -*- coding: utf-8

from django.http import Http404
from django.shortcuts import render
from .models import Work


def work(request, slug, template='works/work.html'):
    try:
        work = Work.objects.published().get(slug=slug)
    except Work.DoesNotExist:
        raise Http404
    return render(request, template, {'work': work})
