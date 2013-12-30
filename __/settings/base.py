"""
Django settings for uranusjr.com

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import unicode_literals
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'blog',
    'pages',
    'works',
    'base',
    'south',
    'compressor',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'markitup',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'base.context_processors.static',
)

ROOT_URLCONF = '__.urls'

WSGI_APPLICATION = '__.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


# Meddia files

MEDIA_URL = '/media/'


# MarkItUp!

MARKITUP_FILTER = ('markdown2.markdown', {'extras': [
    'pyshell', 'fenced-code-blocks', 'wiki-tables', 'smarty-pants'
]})

MARKITUP_PREVIEW_FILTER = MARKITUP_FILTER

MARKITUP_AUTO_PREVIEW = True

MARKITUP_SET = '3rdparty/markitup/sets/markdown-fb'

JQUERY_URL = '3rdparty/jquery/js/jquery-1.10.2.js'


# Grappelli

GRAPPELLI_INDEX_DASHBOARD = '__.dashboard.CustomIndexDashboard'

GRAPPELLI_ADMIN_TITLE = 'Smaller Things'


# FileBrowser

FILEBROWSER_DIRECTORY = ''


# Tastypie

TASTYPIE_DEFAULT_FORMATS = ["json"]
