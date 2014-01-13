#!/usr/bin/env python
# -*- coding: utf-8

from django.test import TestCase, Client
from nose.tools import eq_, assert_not_equal
from django_nose.tools import assert_redirects
from .models import Post


class ViewTests(TestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_blog_index(self):
        # Blog front page should redirect to the latest public page.
        response = self.client.get('/blog/')
        eq_(response.status_code, 302)
        latest = Post.objects.public().latest()
        assert_redirects(response, latest.get_absolute_url())

    def test_post(self):
        posts = Post.objects.all()
        assert_not_equal(posts.count(), 0)
        for post in posts:
            if post.is_public():
                expected = 200
            else:
                expected = 404
            response = self.client.get(post.get_absolute_url())
            eq_(response.status_code, expected)
