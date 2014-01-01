#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render, redirect
from . import feeds
from .models import Post


def index(request):
    # Default to latest public post
    try:
        post = Post.objects.public().latest()
    except Post.DoesNotExist:
        raise Http404
    return redirect(post)


def post(request, pk, slug='', template='blog/post.html'):
    try:
        post = Post.objects.published(
        ).prefetch_related('tags').select_related('category').get(pk=pk)
    except Post.DoesNotExist:
        raise Http404

    if slug != post.slug:   # StackOverflow-style URL canonization
        return redirect(post, permanent=True)
    return render(request, template, {'post': post})


posts_rss201rev2 = feeds.PostsRss201rev2Reed()
posts_atom1 = feeds.PostsAtom1Feed()
