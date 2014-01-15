#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'blog.views',
    url(r'^$', 'index', name='index'),
    url(r'^archive/$', 'post_list', name='post_list'),
    url(r'^category/(?P<slug>.+?)/$', 'category', name='category'),
    url(r'^tag/(?P<slug>.+?)/$', 'tag', name='tag'),
    url(r'^post/(?P<pk>\d+)/$', 'post'),
    url(r'^post/(?P<pk>\d+)/(?P<slug>.+?)/$', 'post', name='post'),
    url(r'^feed/rss201rev2/$', 'posts_rss201rev2', name='posts_rss201rev2'),
    url(r'^feed/atom1/$', 'posts_atom1', name='posts_atom1'),
)
