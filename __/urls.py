#!/usr/bin/env python
# -*- coding: utf-8

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from filebrowser import sites as filebrowser


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^markitup/', include('markitup.urls')),
    url(r'^admin/filebrowser/', include(filebrowser.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^', include('pages.urls', namespace='pages')),
)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
