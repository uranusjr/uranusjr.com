#!/usr/bin/env python
# -*- coding: utf-8

from importlib import import_module
from tastypie.api import Api


def register(api, app_name, resource_name, module_name='resources'):
    module = import_module('.'.join([app_name, module_name]))
    resource_class = getattr(module, resource_name)
    api.register(resource_class())


v1 = Api(api_name='v1')
register(v1, 'blog', 'PostResource')
