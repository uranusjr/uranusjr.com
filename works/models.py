#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField
from base.models import Element, Displayable, Tag as BaseTag


class Category(Element):
    class Meta:
        verbose_name = _('work category')
        verbose_name_plural = _('work categories')


class Tag(BaseTag):
    class Meta:
        verbose_name = _('work tag')
        verbose_name_plural = _('work tags')


class Work(Displayable):

    TYPE_GITHUB = 'github'
    TYPE_BITBUCKET = 'bitbucket'
    TYPE_PRIVATE = 'private'
    TYPE_OTHERS = 'others'

    TYPES = (
        (TYPE_GITHUB, _('GitHub')),
        (TYPE_BITBUCKET, _('BitBucket')),
        (TYPE_PRIVATE, _('Private')),
        (TYPE_OTHERS, _('Others')),
    )

    category = models.ForeignKey(Category, related_name='works')
    tags = models.ManyToManyField(Tag, related_name='works')
    work_type = models.CharField(max_length=9, choices=TYPES)
    image = FileBrowseField(max_length=200, blank=True)
    extra_header_paths = models.ManyToManyField(
        'base.ExtraPath', blank=True, related_name='headered_works'
    )
    extra_footer_paths = models.ManyToManyField(
        'base.ExtraPath', blank=True, related_name='footered_works'
    )

    class Meta:
        verbose_name = _('work')
        verbose_name_plural = _('works')

    def get_absolute_url(self):
        return reverse('works:work', kwargs={'slug': self.slug})

    def tag_slugs(self):
        return [tag.slug for tag in self.tags.all()]
