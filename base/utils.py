#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals


def get_concrete_base_model(model_class, base_class):
    """Find the concrete base class of a given Django model class

    This method traverses the MRO of ``model_class`` to find the derived Django
    model class nearest ``base_class`` that is *not* abstract. If there is no
    such class (i.e. all classes between ``model_class`` and ``base_class`` are
    either abstract or not a Django model, ``None`` is returned.
    """
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


def resolve_value(value):
    """Resolve value from GhostdownField to GhostdownInput
    """
    try:
        return value.raw
    except AttributeError:
        return value or ''
