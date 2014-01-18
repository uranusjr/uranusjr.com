#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'talks.views',
    url(r'^$', 'talk_list', name='talk_list'),
)
