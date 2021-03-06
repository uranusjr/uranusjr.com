#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard
# from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for uranusjr.com.
    """

    def init_with_context(self, context):
        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            collapsible=False,
            column=1,
            exclude=(
                'django.contrib.*',
                'blog.*', 'works.*', 'pages.*', 'talks.*',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Contents'),
            column=1,
            collapsible=False,
            models=(
                'blog.models.Post',
                'talks.models.Talk',
                'works.models.Work',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Pages'),
            column=1,
            collapsible=False,
            models=('pages.*',),
        ))

        self.children.append(modules.ModelList(
            _('Blog'),
            column=1,
            collapsible=False,
            models=(
                'blog.models.Category',
                'blog.models.Tag',
            ),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Talks'),
            column=1,
            collapsible=False,
            models=('talks.models.Tag',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Works'),
            column=1,
            collapsible=False,
            models=('works.models.Category', 'works.models.Tag'),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Administration'),
            column=1,
            collapsible=False,
            models=('django.contrib.*',),
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=3,
            collapsible=False,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))
