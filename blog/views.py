#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import Http404
from django.utils.translation import ugettext as _
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


def category(request, slug, template='blog/post_list.html'):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        raise Http404
    title = _('Posts in category “{title}”').format(title=category.title)
    posts = Post.objects.published().filter(category=category)
    return render(request, template, {
        'title': title, 'obj_list': posts,
    })


def tag(request, slug, template='blog/post_list.html'):
    try:
        tag = Tag.objects.get(slug=slug)
    except Tag.DoesNotExist:
        raise Http404
    title = _('Posts with tag “{name}”').format(name=tag.name)
    posts = Post.objects.published().filter(tags=tag)
    return render(request, template, {
        'title': title, 'obj_list': posts,
    })


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
