#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
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

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ['published_at', 'pk']
        get_latest_by = 'published_at'

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})

    def get_after_query(self, including_self=False):
        pk_q = Q(pk__gte=self.pk) if including_self else Q(pk__gt=self.pk)
        q = ((Q(published_at=self.published_at) & pk_q)
             | Q(published_at__gt=self.published_at))
        return {'filter': q, 'order_by': ('published_at', 'pk')}

    def get_before_query(self, including_self=False):
        pk_q = Q(pk__lte=self.pk) if including_self else Q(pk__lt=self.pk)
        q = ((Q(published_at=self.published_at) & pk_q)
             | Q(published_at__lt=self.published_at))
        return {'filter': q, 'order_by': ('-published_at', '-pk')}

    def after(self):
        p = self.get_after_query()
        return Post.objects.filter(p['filter']).order_by(*p['order_by'])

    def before(self):
        p = self.get_before_query()
        return Post.objects.filter(p['filter']).order_by(*p['order_by'])

    def next(self):
        try:
            post = self.after()[0]
        except IndexError:
            post = None
        return post

    def previous(self):
        try:
            post = self.before()[0]
        except IndexError:
            post = None
        return post
