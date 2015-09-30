#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def static(request):
    less_debug = getattr(settings, 'LESS_DEBUG', settings.DEBUG)
    return {
        'JQUERY_URL': settings.JQUERY_URL,
        'LESS_DEBUG': less_debug,
    }


def site(request):
    return {'current_site': get_current_site(request)}
