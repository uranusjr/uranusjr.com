#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django import template
from works.models import Tag, Work

register = template.Library()


@register.inclusion_tag('works/includes/sidebar.html')
def work_sidebar():
    tags = Tag.objects.filter(works__isnull=False).distinct()
    works = Work.objects.public()
    works = works.select_related('category').prefetch_related('tags')
    return {'tags': tags, 'works': works}
