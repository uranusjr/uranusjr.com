#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import codecs
import os

from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from base.models import Element, Displayable, Tag as BaseTag
from base.utils import render_content


class Category(Element):
    class Meta:
        verbose_name = _('blog category')
        verbose_name_plural = _('blog categories')

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})


class Tag(BaseTag):
    class Meta(BaseTag.Meta):
        verbose_name = _('blog tag')
        verbose_name_plural = _('blog tags')

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})


class Post(Displayable):

    category = models.ForeignKey(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ['published_at', 'pk']
        get_latest_by = 'published_at'

    @property
    def content(self):
        path = finders.find(os.path.join('blog', 'posts', self.slug + '.md'))
        with codecs.open(path, encoding='utf8') as f:
            raw = f.read()
        return mark_safe(render_content(raw))

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.pk, 'slug': self.slug})

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
        public = Post.objects.public()
        return public.filter(p['filter']).order_by(*p['order_by'])

    def before(self):
        p = self.get_before_query()
        public = Post.objects.public()
        return public.filter(p['filter']).order_by(*p['order_by'])

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
