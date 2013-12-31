#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *     # NOQA


SECRET_KEY = get_env_var('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'uranusjr',
        'USER': get_env_var('DB_DEFAULT_LOGIN'),
        'PASSWORD': get_env_var('DB_DEFAULT_PASSWORD'),
        'HOST': get_env_var('DB_DEFAULT_HOST'),
        'PORT': get_env_var('DB_DEFAULT_PORT'),
    },
}

STATIC_ROOT = ''

MEDIA_ROOT = ''
