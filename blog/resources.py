#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import division
from django.core.exceptions import ObjectDoesNotExist
from tastypie import resources, fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound
from tastycrust.resources import ActionResourceMixin, action
from .models import Post, Category


class CategoryResource(resources.ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'blog/category'
        fields = ['title']


class PostResource(ActionResourceMixin, resources.ModelResource):

    category = fields.ToOneField(
        CategoryResource, attribute='category', full=True
    )

    class Meta:
        queryset = Post.objects.published()
        resource_name = 'blog/post'
        fields = [
            'title', 'short_description', 'category', 'tags',
            'published_at',
        ]
        filtering = {
            'slug': resources.ALL,
            'published_at': resources.ALL,
            'before': ('exact',),
            'after': ('exact',),
        }
        ordering = ['published_at']

    def build_filters(self, filters=None):
        """Override to apply custom filters

        We add two custom filters: "before" and "after". Each of them takes a
        post pk, and searches posts before and after the post of that post,
        based on the ['published_at', 'id'] ordering. The custom filters will
        be applied in ``apply_filters``
        """
        before = filters.pop('before', [])
        after = filters.pop('after', [])

        filters = super(PostResource, self).build_filters(filters)

        if before:
            post = Post.objects.get(pk=before[0])
            filters['_before_'] = post.before_query['filter']
        if after:
            post = Post.objects.get(pk=after[0])
            filters['_after_'] = post.after_query['filter']
        return filters

    def apply_filters(self, request, applicable_filters):
        """Override to apply additional rules to ``obj_get_list``

        ``obj_get_list`` should only return "public" posts (not "published"
        posts, which includes private ones), so we need to apply that.

        Custom filters built by ``build_filters`` is applied here
        """
        before_query = applicable_filters.pop('_before_', None)
        after_query = applicable_filters.pop('_after_', None)

        applicable_filters['state'] = Post.STATE_PUBLIC
        objects = super(PostResource, self).apply_filters(
            request, applicable_filters,
        )

        if before_query is not None:
            objects = objects.filter(before_query)
        if after_query is not None:
            objects = objects.filter(after_query)
        return objects

    def dehydrate(self, bundle):
        """Inject extra data into the bundle data

        Fetch object's absolute URL at runtime.
        """
        bundle.data['url'] = bundle.obj.get_absolute_url()
        return bundle

    @action
    def near(self, request, *args, **kwargs):
        try:
            post = self.cached_obj_get(
                self.build_bundle(request), pk=kwargs['pk'],
            )
        except ObjectDoesNotExist:
            raise ImmediateHttpResponse(response=HttpNotFound())
        objects = self.apply_filters(request, {})

        limit = self._meta.limit
        if objects.count() <= limit:    # Not enough entries
            latest = objects.latest()
        else:
            before = post.before()
            after = post.after()
            b_count = before.count()
            a_count = after.count()
            offset = limit // 2
            if b_count < offset:    # Not enough entries before
                # Extend after
                latest = after[limit - b_count - 2]
            elif a_count < offset:  # Not enough entries after
                if a_count > 0:
                    latest = after[a_count - 1]
                else:
                    latest = post
            else:
                latest = after[offset - 1]
        return self.get_list(request, published_at__lte=latest.published_at)
