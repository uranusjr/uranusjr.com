#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import division, unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from tastypie import resources, fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound
from tastycrust.resources import ActionResourceMixin, action
from .models import Post, Category, Tag


class CategoryResource(resources.ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'blog/category'
        fields = ['title', 'slug']


class TagResource(resources.ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'blog/tag'
        fields = ['name', 'slug']


class PostResource(ActionResourceMixin, resources.ModelResource):

    tags = fields.ToManyField(TagResource, attribute='tags', full=True)
    category = fields.ToOneField(
        CategoryResource, attribute='category', full=True
    )

    class Meta:
        queryset = Post.objects.published()
        resource_name = 'blog/post'
        fields = [
            'id', 'title', 'short_description', 'category', 'tags',
            'published_at',
        ]
        filtering = {
            'before': ('exact',),
            'after': ('exact',),
            'including': ('exact',),
        }
        ordering = ['id', 'published_at']

    def build_filters(self, filters=None):
        """Override to apply custom filters

        We add three custom filters: "before", "after", and an optional
        "including" modifier. Each of the first two takes a post pk, and
        searches posts before or after the post of that post, based on the
        ['published_at', 'id'] ordering. "including" serves as an extra
        flag (default to False).

        The custom filters will be applied in ``apply_filters``.
        """
        before = filters.pop('before', [])
        after = filters.pop('after', [])
        including = True if filters.pop('including', None) else False
        filters = super(PostResource, self).build_filters(filters)

        if before:
            post = Post.objects.get(pk=before[0])
            filters['_before_'] = post.get_before_query(including)['filter']
        if after:
            post = Post.objects.get(pk=after[0])
            filters['_after_'] = post.get_after_query(including)['filter']
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

        limit = self._meta.limit
        half_limit = limit // 2
        tail_count = post.before().count()
        front_count = post.after().count()
        if front_count <= half_limit:  # Not enough entries at front
            offset = 0
        elif tail_count < half_limit:  # Not enough entries at tail
            offset = front_count - tail_count - 1
        else:
            offset = front_count - half_limit

        # Floor offset to multiple of limit so that we can get complete pages
        offset = offset // limit * limit

        GET = request.GET.copy()
        GET['offset'] = offset
        GET['order_by'] = '-published_at'
        request.GET = GET
        return self.get_list(request)
