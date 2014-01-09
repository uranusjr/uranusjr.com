#!/usr/bin/env python
# -*- coding: utf-8

from markitup.fields import MarkupField
from markitup.widgets import MarkupHiddenWidget
from ..forms.widgets import GhostdownWidget


class GhostdownField(MarkupField):
    def formfield(self, **kwargs):
        defaults = {'widget': GhostdownWidget}
        defaults.update(kwargs)
        field = super(MarkupField, self).formfield(**defaults)
        field.hidden_widget = MarkupHiddenWidget
        return field
