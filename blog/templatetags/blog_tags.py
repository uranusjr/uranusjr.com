#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django import template
from django.db.models import Count
from blog.models import Category, Tag

register = template.Library()


@register.inclusion_tag('blog/includes/sidebar.html')
def blog_sidebar():
    tags = Tag.objects.annotate(
        post_count=Count('posts')
    ).exclude(post_count=0).order_by('-post_count').distinct()
    categories = Category.objects.annotate(
        post_count=Count('posts')
    ).exclude(post_count=0).order_by('-post_count').distinct()
    return {'tags': tags, 'categories': categories}
