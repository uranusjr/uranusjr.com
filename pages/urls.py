#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.page, kwargs={'slug': 'index'}, name='index'),
    url(r'^talk/', views.talk_list, name='talk_list'),
    url(r'^(?P<slug>.+?)/$', views.page, name='page'),
]
