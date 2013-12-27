#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField
from base.models import Displayable


def _page_image_upload_to(obj, filename):
    return '_'.join([obj.slug, filename])


class Page(Displayable):

    parent = models.ForeignKey(
        'pages.Page', blank=True, null=True, related_name='children',
    )
    image = FileBrowseField(max_length=200, blank=True)

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    def get_absolute_url(self):
        return reverse('pages:page', kwargs={'slug': self.slug})
