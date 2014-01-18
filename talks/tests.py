#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import warnings
from django.test import TestCase
from nose.tools import assert_not_equal
from .utils import OpenGraphImageParser, URLError


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
