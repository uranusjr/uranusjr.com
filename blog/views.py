#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render, redirect
from . import feeds
from .models import Post, Category, Tag


def index(request):
    # Default to latest public post
    try:
        post = Post.objects.public().latest()
    except Post.DoesNotExist:
        raise Http404
    return redirect(post)


def post(request, slug, template='blog/post.html'):
    try:
        post = Post.objects.published().get(slug=slug)
    except Post.DoesNotExist:
        raise Http404
    categories = Category.objects.filter(posts__isnull=False).distinct()
    tags = Tag.objects.filter(posts__isnull=False).distinct()
    return render(request, template, {
        'post': post,
        'categories': categories,
        'tags': tags,
    })


posts_rss201rev2 = feeds.PostsRss201rev2Reed()
posts_atom1 = feeds.PostsAtom1Feed()
