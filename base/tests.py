#!/usr/bin/env python
# -*- coding: utf-8

from django.db import models
from django.test import TestCase
from nose.tools import eq_, assert_raises
from . import utils
from .models import Displayable, ExtraPath


class UtilsTests(TestCase):
    def test_get_concrete_base_model(self):
        with assert_raises(RuntimeError):   # Test for non-model.
            utils.get_concrete_base_model(object, models.Model)
        with assert_raises(RuntimeError):   # Test for abstract model.
            utils.get_concrete_base_model(Displayable, models.Model)

        # Test for model without inheritance relation.
        with assert_raises(RuntimeError):
            utils.get_concrete_base_model(ExtraPath, Displayable)

        eq_(utils.get_concrete_base_model(ExtraPath, models.Model), ExtraPath)
