#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Displayable


def _page_image_upload_to(obj, filename):
    return '_'.join([obj.slug, filename])


class Page(Displayable):

    parent = models.ForeignKey(
        'pages.Page', blank=True, null=True, related_name='children',
    )
    image = models.ImageField(blank=True, null=True, upload_to=_page_image_upload_to)
    extra_header_paths = models.ManyToManyField(
        'base.ExtraPath', blank=True, null=True, related_name='headered_pages'
    )
    extra_footer_paths = models.ManyToManyField(
        'base.ExtraPath', blank=True, null=True, related_name='footered_pages'
    )

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
