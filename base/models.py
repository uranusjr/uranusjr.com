#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _


@python_2_unicode_compatible
class ExtraPath(models.Model):

    TYPE_CSS = 'css'
    TYPE_JAVASCRIPT = 'javascript'

    TYPES = (
        (TYPE_CSS, _('CSS')),
        (TYPE_JAVASCRIPT, _('JavaScript')),
    )

    link_type = models.CharField(max_length=10, choices=TYPES)
    path = models.FilePathField(unique=True)

    class Meta:
        verbose_name = _('extra path')
        verbose_name_plural = _('extra paths')

    def __str__(self):
        return ugettext('{model_name} at {path}').format(
            model_name=self._meta.verbose_name.capitalize(),
            path=self.path,
        )


@python_2_unicode_compatible
class Tag(models.Model):

    name = models.CharField(max_length=50)

    class Meta:
        abstract = True
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return ugettext('{model_name} {name}').format(
            model_name=self._meta.verbose_name.capitalize(),
            name=self.name,
        )


@python_2_unicode_compatible
class Element(models.Model):

    title = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        abstract = True
        verbose_name = _('element')
        verbose_name_plural = _('elements')

    def __str__(self):
        return ugettext('{model_name} {title}').format(
            model_name=self._meta.verbose_name.capitalize(),
            title=self.title,
        )


class DisplayableManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(
            state__in=(Displayable.STATE_PUBLIC, Displayable.STATE_PRIVATE),
            published_at__lte=datetime.date.today(),
        )

    def public(self):
        return self.get_queryset().filter(
            state=Displayable.STATE_PUBLIC,
            published_at__lte=datetime.date.today(),
        )


class Displayable(Element):

    STATE_DRAFT = 'draft'
    STATE_PUBLIC = 'public'
    STATE_PRIVATE = 'private'

    STATES = (
        (STATE_DRAFT, _('Draft')),
        (STATE_PUBLIC, _('Public')),
        (STATE_PRIVATE, _('Private')),
    )

    state = models.CharField(max_length=7, choices=STATES, default=STATE_DRAFT)
    published_at = models.DateField(default=datetime.date.today)
    short_description = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    objects = DisplayableManager()

    class Meta:
        abstract = True
        verbose_name = _('displayable')
        verbose_name_plural = _('displayables')
