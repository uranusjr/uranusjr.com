#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models.query import QuerySet
from django.utils.timezone import now


class DisplayableQuerySet(QuerySet):
    """Custom QuerySet subclass for Displayable descendants

    This class requires the model using it implementing at least two fields,
    ``state`` and ``published_at`` (a DateTimeField), and two extra attributes
    ``STATE_PUBLIC`` and ``STATE_PRIVATE``.
    """
    def published(self):
        return self.filter(
            state__in=(self.model.STATE_PUBLIC, self.model.STATE_PRIVATE),
            published_at__lte=now(),
        )

    def public(self):
        return self.filter(
            state=self.model.STATE_PUBLIC,
            published_at__lte=now(),
        )
