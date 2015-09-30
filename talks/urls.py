#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.talk_list, name='talk_list'),
    url(r'^tag/(?P<slug>.+?)/$', views.tag, name='tag'),
]
