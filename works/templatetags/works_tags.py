#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django import template
from django.db.models import Count
from works.models import Tag, Work

register = template.Library()


@register.inclusion_tag('works/includes/sidebar.html', takes_context=True)
def work_sidebar(context):
    tags = Tag.objects.annotate(
        work_count=Count('works')
    ).exclude(work_count=0).order_by('-work_count').distinct()
    works = Work.objects.public()
    works = works.select_related('category').prefetch_related('tags')
    return {
        'current_site': context['current_site'],
        'tags': tags, 'works': works,
    }
