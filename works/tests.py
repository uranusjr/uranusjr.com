#!/usr/bin/env python
# -*- coding: utf-8

from django.test import TestCase, Client
from nose.tools import eq_, assert_not_equal
from .models import Work


class ViewTests(TestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_work(self):
        works = Work.objects.all()
        assert_not_equal(works.count(), 0)
        for work in works:
            if work.is_public():
                expected = 200
            else:
                expected = 404
            response = self.client.get(work.get_absolute_url())
            eq_(response.status_code, expected)
