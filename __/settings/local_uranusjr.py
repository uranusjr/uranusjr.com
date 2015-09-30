#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from .base import *     # NOQA


DEBUG = True

SECRET_KEY = 'i=sp#p$s^dwm6etgercjjo4$0t77#^=!t6v4sb61ad+^tcy@)i'

INSTALLED_APPS += [
    'debug_toolbar',
    'django_nose',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--cover-package=base,blog,pages,talks,works',
    '--with-coverage',
    '--cover-erase',
]
