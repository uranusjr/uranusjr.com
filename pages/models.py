#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField
from base.models import Displayable, Orderable


def _page_image_upload_to(obj, filename):
    return '_'.join([obj.slug, filename])


class Page(Orderable, Displayable):

    parent = models.ForeignKey(
        'pages.Page', blank=True, null=True, related_name='children',
    )
    _root = models.ForeignKey(
        'pages.Page', blank=True, null=True, related_name='descendants',
    )
    image = FileBrowseField(max_length=200, blank=True)

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ['parent__order', 'parent__pk', 'order', 'pk']

    def get_absolute_url(self):
        return reverse('pages:page', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Update the page's own, and all its descendants' ``_root``s when the
        # page switches to another parent
        try:
            old_object = Page.objects.get(pk=self.pk)
        except Page.DoesNotExist:
            # No match, so this is an INSERT; just set the root
            self._root = self.parent
            pass
        else:
            # This is an UPDATE
            if old_object.parent != self.parent:
                if self.parent is None:
                    new_root = None
                else:
                    new_root = self.parent._root
                self._root = new_root
                self.descendants.all().update(_root=new_root)
        return super(Page, self).save(*args, **kwargs)
