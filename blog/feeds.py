#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.utils import feedgenerator
from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.views import Feed
from pages.models import Page
from .models import Post


class PostsFeed(Feed):
    """Common parent class for RSS and Atom feeds
    """

    title = _('Smaller Things from an Insignificant One')

    def description(self):
        try:
            index_page = Page.objects.get(slug='index')
        except Post.DoesNotExist:
            return ''
        else:
            return index_page.content

    def link(self):
        return reverse('blog:index')

    def items(self):
        return Post.objects.public()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.published_at

    def item_categories(self, item):
        categories = [tag.name for tag in item.tags.all()]
        categories.insert(0, item.category.title)
        return categories


class PostsRss201rev2Reed(PostsFeed):
    feed_type = feedgenerator.Rss201rev2Feed


class PostsAtom1Feed(PostsFeed):
    feed_type = feedgenerator.Atom1Feed
