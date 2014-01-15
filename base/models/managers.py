#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from .query import DisplayableQuerySet


class DisplayableManager(models.Manager):

    use_for_related_fields = True

    def get_queryset(self):
        return DisplayableQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def public(self):
        return self.get_queryset().public()
