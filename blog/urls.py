#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^archive/$', views.post_list, name='post_list'),
    url(r'^category/(?P<slug>.+?)/$', views.category, name='category'),
    url(r'^tag/(?P<slug>.+?)/$', views.tag, name='tag'),
    url(r'^post/(?P<pk>\d+)/$', views.post),
    url(r'^post/(?P<pk>\d+)/(?P<slug>.+?)/$', views.post, name='post'),
    url(r'^feed/rss201rev2/$', views.posts_rss201r2, name='posts_rss201r2'),
    url(r'^feed/atom1/$', views.posts_atom1, name='posts_atom1'),
]
