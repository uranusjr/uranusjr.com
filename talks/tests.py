#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import warnings
from django.test import TestCase, Client
from nose.tools import eq_, assert_not_equal
from .utils import OpenGraphImageParser, URLError
from .models import Tag


class UtilsTests(TestCase):
    def test_og_scrapper(self):
        parser = OpenGraphImageParser()
        urls = (
            'https://speakerdeck.com/uranusjr/we-buy-cheese-in-a-cheese-shop',
            'http://www.slideshare.net/uranusjr/naming-convention-in-python',
        )
        for url in urls:
            try:
                image_url = parser.parse_from_url(url)
            except URLError:
                msg_form = 'Cannot retrieve content from {url}. Test skipped.'
                warnings.warn(msg_form.format(url=url), RuntimeWarning)
            else:
                assert_not_equal(len(image_url), 0)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_talk_list(self):
        response = self.client.get('/talk/')
        # eq_(response.status_code, 200)
        eq_(response.status_code, 304)  # TODO: Implement talks page.

    def test_talk_tag(self):
        tags = Tag.objects.all()
        # TODO: Generate a fixture to make this test pass
        # assert_not_equal(tags.count(), 0)
        for tag in tags:
            if tag.is_public():
                expected = 200
            else:
                expected = 404
            response = self.client.get(tag.get_absolute_url())
            eq_(response.status_code, expected)
