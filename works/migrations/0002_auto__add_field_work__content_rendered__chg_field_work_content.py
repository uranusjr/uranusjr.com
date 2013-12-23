# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Work._content_rendered'
        db.add_column(u'works_work', '_content_rendered',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'Work.content'
        db.alter_column(u'works_work', 'content', self.gf('markitup.fields.MarkupField')(no_rendered_field=True))

    def backwards(self, orm):
        # Deleting field 'Work._content_rendered'
        db.delete_column(u'works_work', '_content_rendered')


        # Changing field 'Work.content'
        db.alter_column(u'works_work', 'content', self.gf('django.db.models.fields.TextField')())

    models = {
        u'base.extrapath': {
            'Meta': {'object_name': 'ExtraPath'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path': ('django.db.models.fields.FilePathField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'works.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'works.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'works.work': {
            'Meta': {'object_name': 'Work'},
            '_content_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'works'", 'to': u"orm['works.Category']"}),
            'content': ('markitup.fields.MarkupField', [], {'no_rendered_field': 'True', 'blank': 'True'}),
            'extra_footer_paths': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'footered_works'", 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            'extra_header_paths': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'headered_works'", 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '7'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'works'", 'symmetrical': 'False', 'to': u"orm['works.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'work_type': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        }
    }

    complete_apps = ['works']