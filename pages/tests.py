#!/usr/bin/env python
# -*- coding: utf-8

from django.test import TestCase, Client
from nose.tools import eq_, assert_not_equal
from .models import Page


class ViewTests(TestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_page(self):
        pages = Page.objects.all()
        assert_not_equal(pages.count(), 0)
        for page in pages:
            if not page.is_public():
                expected = 404
            elif page.slug in ('blog', 'index',):
                # Blog front page is explicitly redirected to the latest post.
                # We test this is the blog app, so this is just special-cased.
                # The index page is special-cased to redirect to pages:index.
                expected = 302
            else:
                expected = 200
            response = self.client.get(page.get_absolute_url())
            eq_(response.status_code, expected)

    def test_index(self):
        eq_(self.client.get('/').status_code, 200)
