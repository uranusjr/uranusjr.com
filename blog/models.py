#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Element, Displayable, Tag as BaseTag


class Category(Element):
    class Meta:
        verbose_name = _('blog category')
        verbose_name_plural = _('blog categories')


class Tag(BaseTag):
    class Meta:
        verbose_name = _('blog tag')
        verbose_name_plural = _('blog tags')


class Post(Displayable):

    category = models.ForeignKey(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    extra_header_paths = models.ManyToManyField(
        'base.ExtraPath', blank=True, related_name='headered_blog_posts'
    )
    extra_footer_paths = models.ManyToManyField(
        'base.ExtraPath', blank=True, related_name='footered_blog_posts'
    )

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        get_latest_by = 'published_at'

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})

    def next(self):
        filters = {'published_at__gt': self.published_at}
        try:
            public = Post.objects.public()
            post = public.filter(**filters).order_by('published_at')[0]
        except IndexError:
            post = None
        return post

    def previous(self):
        filters = {'published_at__lt': self.published_at}
        try:
            public = Post.objects.public()
            post = public.filter(**filters).order_by('-published_at')[0]
        except IndexError:
            post = None
        return post
