#!/usr/bin/env python
# -*- coding: utf-8

from django.conf import settings


def static(request):
    return {'JQUERY_URL': settings.JQUERY_URL}
