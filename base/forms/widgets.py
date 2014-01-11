#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.template.loader import get_template
from ghostdown.forms.widgets import GhostdownInput


class PopupGhostdownInput(GhostdownInput):
    template = get_template('base/includes/ghostdown_editor.html')
