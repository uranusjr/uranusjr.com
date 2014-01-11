#!/usr/bin/env python
# -*- coding: utf-8

from markitup.fields import MarkupField
from markitup.widgets import MarkupHiddenWidget
from ghostdown.forms.widgets import GhostdownInput


class GhostdownField(MarkupField):
    def formfield(self, **kwargs):
        defaults = {'widget': GhostdownInput(value_key='raw')}
        defaults.update(kwargs)
        field = super(MarkupField, self).formfield(**defaults)
        field.hidden_widget = MarkupHiddenWidget
        return field
