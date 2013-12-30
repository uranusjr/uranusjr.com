#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf import settings


def static(request):
    less_debug = getattr(settings, 'LESS_DEBUG', settings.DEBUG)
    return {
        'JQUERY_URL': settings.JQUERY_URL,
        'LESS_DEBUG': less_debug,
    }
