#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import Displayable, Tag as BaseTag

from .utils import OpenGraphImageParser, URLError


class Tag(BaseTag):
    class Meta(BaseTag.Meta):
        verbose_name = _('talk tag')
        verbose_name_plural = _('talk tags')

    def get_absolute_url(self):
        return reverse('talks:tag', kwargs={'slug': self.slug})


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
            if not self.image_url:
                # Only scrape for a image when the user has left the field
                # blank. If the user has provided a value, we should honor it.
                self.image_url = self.scrape_image_from_url()
        else:
            # This is an UPDATE.
            if (self.url != old_object.url
                    and self.image_url == old_object.image_url):
                # URL has changed but the image has not (which makes it
                # obsolute). If the image has changed the user probably knows
                # what's going on, so we leave it be.
                self.image_url = self.scrape_image_from_url()
        super(Talk, self).save(*args, **kwargs)

    def scrape_image_from_url(self):
        # Try to scrape the presentation hosting site for og:image
        parser = OpenGraphImageParser()
        try:
            image_url = parser.parse_from_url(self.url)
        except URLError:
            image_url = ''
        return image_url
