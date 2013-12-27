#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals


def get_concrete_base_model(model_class, base_class):
    try:
        assert (
            not model_class._meta.abstract
            and issubclass(model_class, base_class)
        )
    except AssertionError:
        raise RuntimeError(
            '{child} should be a concrete subclass of {parent}'.format(
                child=model_class, parent=base_class
            )
        )
    for klass in reversed(model_class.mro()):
        if issubclass(klass, base_class) and not klass._meta.abstract:
            return klass
