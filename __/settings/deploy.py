#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *     # NOQA

ALLOWED_HOSTS = ['uranusjr.com']

SECRET_KEY = get_env_var('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_var('DB_DEFAULT_NAME'),
        'USER': get_env_var('DB_DEFAULT_LOGIN'),
        'PASSWORD': get_env_var('DB_DEFAULT_PASSWORD'),
        'HOST': get_env_var('DB_DEFAULT_HOST'),
        'PORT': get_env_var('DB_DEFAULT_PORT'),
    },
}

STATIC_ROOT = get_env_var('STATIC_ROOT')

MEDIA_ROOT = get_env_var('MEDIA_ROOT')