# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Post.slug'
        db.alter_column(u'blog_post', 'slug', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Removing index on 'Post', fields ['slug']
        db.delete_index(u'blog_post', ['slug'])


        # Changing field 'Post.published_at'
        db.alter_column(u'blog_post', 'published_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Category.slug'
        db.alter_column(u'blog_category', 'slug', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Removing index on 'Category', fields ['slug']
        db.delete_index(u'blog_category', ['slug'])


    def backwards(self, orm):
        # Adding index on 'Category', fields ['slug']
        db.create_index(u'blog_category', ['slug'])

        # Adding index on 'Post', fields ['slug']
        db.create_index(u'blog_post', ['slug'])


        # Changing field 'Post.slug'
        db.alter_column(u'blog_post', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

        # Changing field 'Post.published_at'
        db.alter_column(u'blog_post', 'published_at', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Category.slug'
        db.alter_column(u'blog_category', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

    models = {
        u'base.extrapath': {
            'Meta': {'object_name': 'ExtraPath'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path': ('django.db.models.fields.FilePathField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'blog.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blog.post': {
            'Meta': {'object_name': 'Post'},
            '_content_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'posts'", 'to': u"orm['blog.Category']"}),
            'content': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'extra_footer_paths': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'footered_blog_posts'", 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            'extra_header_paths': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'headered_blog_posts'", 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '7'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'posts'", 'blank': 'True', 'to': u"orm['blog.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blog.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['blog']