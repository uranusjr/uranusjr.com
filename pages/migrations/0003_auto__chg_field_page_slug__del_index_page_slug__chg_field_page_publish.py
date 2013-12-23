# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Page.slug'
        db.alter_column(u'pages_page', 'slug', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Removing index on 'Page', fields ['slug']
        db.delete_index(u'pages_page', ['slug'])


        # Changing field 'Page.published_at'
        db.alter_column(u'pages_page', 'published_at', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):
        # Adding index on 'Page', fields ['slug']
        db.create_index(u'pages_page', ['slug'])


        # Changing field 'Page.slug'
        db.alter_column(u'pages_page', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

        # Changing field 'Page.published_at'
        db.alter_column(u'pages_page', 'published_at', self.gf('django.db.models.fields.DateField')())

    models = {
        u'base.extrapath': {
            'Meta': {'object_name': 'ExtraPath'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path': ('django.db.models.fields.FilePathField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'pages.page': {
            'Meta': {'object_name': 'Page'},
            '_content_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'extra_footer_paths': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'footered_pages'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            'extra_header_paths': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'headered_pages'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['pages.Page']"}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '7'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pages']