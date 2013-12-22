# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table(u'pages_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(default=u'draft', max_length=7)),
            ('published_at', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'children', null=True, to=orm['pages.Page'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'pages', ['Page'])

        # Adding M2M table for field extra_header_paths on 'Page'
        m2m_table_name = db.shorten_name(u'pages_page_extra_header_paths')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm[u'pages.page'], null=False)),
            ('extrapath', models.ForeignKey(orm[u'base.extrapath'], null=False))
        ))
        db.create_unique(m2m_table_name, ['page_id', 'extrapath_id'])

        # Adding M2M table for field extra_footer_paths on 'Page'
        m2m_table_name = db.shorten_name(u'pages_page_extra_footer_paths')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm[u'pages.page'], null=False)),
            ('extrapath', models.ForeignKey(orm[u'base.extrapath'], null=False))
        ))
        db.create_unique(m2m_table_name, ['page_id', 'extrapath_id'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table(u'pages_page')

        # Removing M2M table for field extra_header_paths on 'Page'
        db.delete_table(db.shorten_name(u'pages_page_extra_header_paths'))

        # Removing M2M table for field extra_footer_paths on 'Page'
        db.delete_table(db.shorten_name(u'pages_page_extra_footer_paths'))


    models = {
        u'base.extrapath': {
            'Meta': {'object_name': 'ExtraPath'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path': ('django.db.models.fields.FilePathField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'pages.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'extra_footer_paths': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'footered_pages'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            'extra_header_paths': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'headered_pages'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['pages.Page']"}),
            'published_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '7'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pages']