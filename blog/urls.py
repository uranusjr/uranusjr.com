#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'blog.views',
    url(r'^$', 'index', name='index'),
    url(r'^post/(?P<slug>.*?)/$', 'post', name='post'),
    url(r'^feed/rss201rev2/$', 'posts_rss201rev2', name='post_rss201rev2'),
    url(r'^feed/atom1/$', 'posts_atom1', name='posts_atom1'),
)
