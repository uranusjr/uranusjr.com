#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'works.views',
    url(r'^(?P<slug>.+?)/$', 'work', name='work'),
)
