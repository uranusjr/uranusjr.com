#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Displayable, Tag as BaseTag
from .utils import OpenGraphImageParser


class Tag(BaseTag):
    class Meta:
        verbose_name = _('talk tag')
        verbose_name_plural = _('talk tags')


class Talk(Displayable):

    tags = models.ManyToManyField(Tag, blank=True, related_name='talks')
    url = models.URLField(
        verbose_name=_('URL'),
        help_text=_('URL to the slides on a presentation hosting site.')
    )
    image_url = models.URLField(
        blank=True,
        verbose_name=_('URL to cover image'),
    )

    class Meta:
        verbose_name = _('talk')
        verbose_name_plural = _('talks')
        ordering = ['published_at', 'pk']

    def save(self, *args, **kwargs):
        try:
            old_object = Talk.objects.get(pk=self.pk)
        except Talk.DoesNotExist:
            # No match; this is an INSERT.
            self.image_url = self.scrape_image_from_url()
        else:
            # This is an UPDATE
            if self.url != old_object.url:
                self.image_url = self.scrape_image_from_url()
        super(Talk, self).save(*args, **kwargs)

    def scrape_image_from_url(self):
        # Try to scrape the presentation hosting site for og:image
        parser = OpenGraphImageParser()
        parser.parse_from_url(self.url)
        return parser.og_image or ''
