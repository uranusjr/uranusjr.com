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
    if request.user.is_superuser:
        published = Post.objects.all()
    else:
        published = Post.objects.published()
    published = published.prefetch_related('tags').select_related('category')
    try:
        post = published.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404

    if slug != post.slug:   # StackOverflow-style URL canonization
        return redirect(post, permanent=True)
    return render(request, template, {'post': post})


class PostListView(DisplayableListView):

    template_name = 'post_list.html'

    def get_queryset(self):
        posts = Post.objects.published()
        return posts.order_by('-published_at', '-pk')

    def get_title(self):
        return _('Blog archive')


class CategoryPostListView(PostListView):
    def get(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(slug=kwargs['slug'])
        except Category.DoesNotExist:
            raise Http404
        return super(CategoryPostListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        posts = super(CategoryPostListView, self).get_queryset()
        return posts.filter(category=self.category)

    def get_title(self):
        title_format = _('Posts in category “{title}”')
        return title_format.format(title=self.category.title)


class TagPostListView(PostListView):
    def get(self, request, *args, **kwargs):
        try:
            self.tag = Tag.objects.get(slug=kwargs['slug'])
        except Tag.DoesNotExist:
            raise Http404
        return super(TagPostListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        posts = super(TagPostListView, self).get_queryset()
        return posts.filter(tags=self.tag)

    def get_title(self):
        title_format = _('Posts with tag “{name}”')
        return title_format.format(name=self.tag.name)


post_list = PostListView.as_view()
category = CategoryPostListView.as_view()
tag = TagPostListView.as_view()
posts_rss201rev2 = feeds.PostsRss201rev2Reed()
posts_atom1 = feeds.PostsAtom1Feed()
