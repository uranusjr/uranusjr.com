#!/usr/bin/env python
# -*- coding: utf-8

from markitup.fields import MarkupField
from markitup.widgets import MarkupHiddenWidget
from ghostdown.forms.widgets import GhostdownInput
from ..utils import resolve_value


class GhostdownField(MarkupField):
    def formfield(self, **kwargs):
        defaults = {'widget': GhostdownInput(resolve_value=resolve_value)}
        defaults.update(kwargs)
        field = super(MarkupField, self).formfield(**defaults)
        field.hidden_widget = MarkupHiddenWidget
        return field
