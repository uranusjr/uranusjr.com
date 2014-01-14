#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import Http404
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from base.views import DisplayableListView
from . import feeds
from .models import Post, Category, Tag


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


class CategoryPostListView(DisplayableListView):

    template_name = 'post_list.html'

    def get(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(slug=kwargs['slug'])
        except Category.DoesNotExist:
            raise Http404
        return super(CategoryPostListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        posts = Post.objects.published().filter(category=self.category)
        return posts.order_by('-published_at', '-pk')

    def get_context_data(self, **kwargs):
        context = super(CategoryPostListView, self).get_context_data(**kwargs)
        title_format = _('Posts in category “{title}”')
        context['title'] = title_format.format(title=self.category.title)
        return context


class TagPostListView(DisplayableListView):

    template_name = 'post_list.html'

    def get(self, request, *args, **kwargs):
        try:
            self.tag = Tag.objects.get(slug=kwargs['slug'])
        except Tag.DoesNotExist:
            raise Http404
        return super(TagPostListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        posts = Post.objects.published().filter(tags=self.tag)
        return posts.order_by('-published_at', '-pk')

    def get_context_data(self, **kwargs):
        context = super(CategoryPostListView, self).get_context_data(**kwargs)
        title_format = _('Posts with tag “{name}”')
        context['title'] = title_format.format(title=self.tag.name)
        return context


category = CategoryPostListView.as_view()
tag = TagPostListView.as_view()
posts_rss201rev2 = feeds.PostsRss201rev2Reed()
posts_atom1 = feeds.PostsAtom1Feed()
