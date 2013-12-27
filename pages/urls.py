#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'pages.views',
    url(r'^$', 'page', kwargs={'slug': 'index'}, name='index'),
    url(r'^(?P<slug>.*?)/$', 'page', name='page'),
)
