#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
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
    tags = models.ManyToManyField(Tag, related_name='posts')
    extra_header_paths = models.ManyToManyField(
        'base.ExtraPath', related_name='headered_blog_posts'
    )
    extra_footer_paths = models.ManyToManyField(
        'base.ExtraPath', related_name='footered_blog_posts'
    )

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        get_latest_by = 'published_at'
