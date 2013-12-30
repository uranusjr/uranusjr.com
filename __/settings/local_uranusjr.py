#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from .base import *     # NOQA


DEBUG = True

SECRET_KEY = 'i=sp#p$s^dwm6etgercjjo4$0t77#^=!t6v4sb61ad+^tcy@)i'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media', 'static')
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

INSTALLED_APPS += (
    'debug_toolbar',
)
