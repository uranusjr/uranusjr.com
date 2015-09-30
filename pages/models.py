#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import codecs
import os

from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from filebrowser.fields import FileBrowseField

from base.models import Displayable, Orderable
from base.utils import render_content


def _page_image_upload_to(obj, filename):
    return '_'.join([obj.slug, filename])


class Page(Orderable, Displayable):

    parent = models.ForeignKey(
        'pages.Page', blank=True, null=True, related_name='children',
    )
    _root = models.ForeignKey(
        'pages.Page', blank=True, null=True,
        related_name='descendants_with_self',
    )
    image = FileBrowseField(max_length=200, blank=True)
    image_caption = models.TextField(
        blank=True, help_text=_('Can contain HTML tags')
    )

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ['parent__order', 'parent__pk', 'order', 'pk']

    @property
    def content(self):
        path = finders.find(os.path.join('pages', 'posts', self.slug + '.md'))
        with codecs.open(path, encoding='utf8') as f:
            raw = f.read()
        return mark_safe(render_content(raw))

    def get_absolute_url(self):
        return reverse('pages:page', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Update the page's own, and all its descendants' ``_root``s when the
        # page switches to another parent
        try:
            old_object = Page.objects.get(pk=self.pk)
        except Page.DoesNotExist:
            # No match, so this is an INSERT; just set the root.
            self._root = self.parent._root or self
        else:
            # This is an UPDATE with parent change.
            parent = self.parent
            if old_object.parent != parent:
                if parent is None:      # I am the root!
                    new_root = self
                else:
                    new_root = parent._root
                self.descendants.all().update(_root=new_root)
                self._root = new_root
        return super(Page, self).save(*args, **kwargs)

    @property
    def descendants(self):
        return self.descendants_with_self.exclude(pk=self.pk)

    def get_icon_url(self):
        if self.image:
            return self.image.url
        else:
            return finders.find(os.path.join('base', 'img', 'circle.png'))
