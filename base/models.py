#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.db.models import Max
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.contenttypes.generic import GenericForeignKey
from filebrowser.fields import FileBrowseField
from ghostdown.models.fields import GhostdownField
from .utils import get_concrete_base_model


@python_2_unicode_compatible
class ExtraPath(models.Model):

    FILE_TYPE_CSS = 'css'
    FILE_TYPE_JAVASCRIPT = 'javascript'

    FILE_TYPES = (
        (FILE_TYPE_CSS, _('CSS')),
        (FILE_TYPE_JAVASCRIPT, _('JavaScript')),
    )

    LINK_TYPE_HEADER = 0
    LINK_TYPE_FOOTER = 1

    LINK_TYPES = (
        (LINK_TYPE_HEADER, _('Header')),
        (LINK_TYPE_FOOTER, _('Footer')),
    )

    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    link_type = models.IntegerField(
        default=LINK_TYPE_HEADER, choices=LINK_TYPES
    )
    target = FileBrowseField(max_length=200, extensions=['.css', '.js'])

    owner_type = models.ForeignKey('contenttypes.ContentType')
    owner_id = models.PositiveIntegerField()
    owner = GenericForeignKey('owner_type', 'owner_id')

    class Meta:
        verbose_name = _('extra path')
        verbose_name_plural = _('extra paths')

    def __str__(self):
        return ugettext('{link} {file} at {path}').format(
            link=self.get_link_type_display(),
            file=self.get_file_type_display(),
            path=self.target
        )


@python_2_unicode_compatible
class Tag(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Element(models.Model):

    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True
        verbose_name = _('element')
        verbose_name_plural = _('elements')

    def __str__(self):
        return self.title


class Orderable(models.Model):

    order = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_('order')
    )

    class Meta:
        abstract = True
        verbose_name = _('orderable')
        verbose_name_plural = _('orderables')
        ordering = ['order', 'pk']

    def save(self, *args, **kwargs):
        """Overriden from Model

        Provides initial ordering value.
        """
        if self.order is None:
            klass = get_concrete_base_model(type(self), Orderable)
            max_order = klass.objects.aggregate(
                max_order=Max('order')
            )['max_order']
            if max_order is None:
                max_order = -1
            self.order = max_order + 1
        super(Orderable, self).save(*args, **kwargs)


class DisplayableManager(models.Manager):

    use_for_related_fields = True

    def published(self):
        return self.get_queryset().filter(
            state__in=(Displayable.STATE_PUBLIC, Displayable.STATE_PRIVATE),
            published_at__lte=now(),
        )

    def public(self):
        return self.get_queryset().filter(
            state=Displayable.STATE_PUBLIC,
            published_at__lte=now(),
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
    published_at = models.DateTimeField(default=now)
    short_description = models.CharField(max_length=200)
    content = GhostdownField(blank=True)

    objects = DisplayableManager()

    class Meta:
        abstract = True
        verbose_name = _('displayable')
        verbose_name_plural = _('displayables')
