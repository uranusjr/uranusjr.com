#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import render
from .models import Post


def post(request, slug, template='blog/post.html'):
    try:
        if slug is None:    # Default to latest public post
            post = Post.objects.public().latest()
        else:
            post = Post.objects.published().get(slug=slug)
    except Post.DoesNotExist:
        raise Http404
    return render(request, template, {'post': post})
