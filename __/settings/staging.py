#!/usr/bin/env python
# -*- coding: utf-8

from .base import *     # NOQA


SECRET_KEY = 'i=sp#p$s^dwm6etgercjjo4$0t77#^=!t6v4sb61ad+^tcy@)i'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
