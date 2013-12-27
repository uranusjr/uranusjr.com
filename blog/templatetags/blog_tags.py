#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django import template
from blog.models import Category, Tag

register = template.Library()


@register.inclusion_tag('blog/includes/sidebar.html')
def blog_sidebar():
    tags = Tag.objects.filter(posts__isnull=False).distinct()
    categories = Category.objects.filter(posts__isnull=False).distinct()
    return {'tags': tags, 'categories': categories}
