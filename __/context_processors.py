#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf import settings


def static(request):
    return {'JQUERY_URL': settings.JQUERY_URL}
