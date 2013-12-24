#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import render, redirect
from .models import Post


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
    return render(request, template, {'post': post})
