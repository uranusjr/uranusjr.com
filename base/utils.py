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
            issubclass(model_class, base_class)
            and not model_class._meta.abstract
        )
    except AssertionError:
        raise RuntimeError(
            '{child} should be a concrete subclass of {parent}'.format(
                child=model_class, parent=base_class
            )
        )
    for klass in reversed(model_class.mro()):
        if not issubclass(klass, base_class):
            continue
        if not hasattr(klass, '_meta'):
            continue
        if klass._meta.abstract:
            continue
        return klass
