#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from filebrowser import sites as filebrowser

from .api import v1


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(filebrowser.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^work/', include('works.urls', namespace='works')),
    url(r'^', include('pages.urls', namespace='pages')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
