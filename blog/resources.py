#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import division
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
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
        }
        ordering = ['-published_at']

    def apply_filters(self, request, applicable_filters):
        """Override apply_filters to apply additional filters

        We can apply additional filters here because this is only called by
        ``obj_get_list``. ``obj_get_list`` should only return "public" posts
        (not "published" posts, which includes private ones), so we need to
        apply that.
        """
        applicable_filters['state'] = Post.STATE_PUBLIC
        return super(PostResource, self).apply_filters(
            request, applicable_filters,
        )

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
            before = objects.filter(
                Q(published_at__lt=post.published_at)
                | Q(published_at=post.published_at, pk__gt=post.pk)
            ).order_by('-published_at', 'pk')
            after = objects.filter(
                Q(published_at__gt=post.published_at)
                | Q(published_at=post.published_at, pk__lt=post.pk)
            ).order_by('published_at', '-pk')

            b_count = before.count()
            a_count = after.count()
            offset = limit // 2
            print b_count, a_count, offset
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
