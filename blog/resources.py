#!/usr/bin/env python
# -*- coding: utf-8

from tastypie import resources
from .models import Post


class PostResource(resources.ModelResource):
    class Meta:
        queryset = Post.objects.published()
        resource_name = 'blog/post'
        fields = [
            'title', 'short_description', 'category', 'tags',
            'published_at'
        ]

    def apply_filters(self, request, applicable_filters):
        """Override apply_filters to apply additional filters

        We can apply additional filters here because this is only called by
        ``obj_get_list``. ``obj_get_list`` should only return "public" posts
        (not "published" posts, which includes private ones), so we need to
        apply that.
        """
        applicable_filters['state'] = Post.STATE_PUBLIC
        return super(PostResource, self).apply_filters(
            request, applicable_filters
        )

    def dehydrate(self, bundle):
        """Inject extra data into the bundle data

        Fetch object's absolute URL at runtime.
        """
        bundle.data['url'] = bundle.obj.get_absolute_url()
        return bundle
