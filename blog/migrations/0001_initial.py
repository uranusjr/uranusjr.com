# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'blog_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'blog', ['Category'])

        # Adding model 'Tag'
        db.create_table(u'blog_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'blog', ['Tag'])

        # Adding model 'Post'
        db.create_table(u'blog_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(default=u'draft', max_length=7)),
            ('published_at', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'posts', to=orm['blog.Category'])),
        ))
        db.send_create_signal(u'blog', ['Post'])

        # Adding M2M table for field tags on 'Post'
        m2m_table_name = db.shorten_name(u'blog_post_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'blog.post'], null=False)),
            ('tag', models.ForeignKey(orm[u'blog.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'tag_id'])

        # Adding M2M table for field extra_header_paths on 'Post'
        m2m_table_name = db.shorten_name(u'blog_post_extra_header_paths')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'blog.post'], null=False)),
            ('extrapath', models.ForeignKey(orm[u'base.extrapath'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'extrapath_id'])

        # Adding M2M table for field extra_footer_paths on 'Post'
        m2m_table_name = db.shorten_name(u'blog_post_extra_footer_paths')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'blog.post'], null=False)),
            ('extrapath', models.ForeignKey(orm[u'base.extrapath'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'extrapath_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'blog_category')

        # Deleting model 'Tag'
        db.delete_table(u'blog_tag')

        # Deleting model 'Post'
        db.delete_table(u'blog_post')

        # Removing M2M table for field tags on 'Post'
        db.delete_table(db.shorten_name(u'blog_post_tags'))

        # Removing M2M table for field extra_header_paths on 'Post'
        db.delete_table(db.shorten_name(u'blog_post_extra_header_paths'))

        # Removing M2M table for field extra_footer_paths on 'Post'
        db.delete_table(db.shorten_name(u'blog_post_extra_footer_paths'))


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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blog.post': {
            'Meta': {'object_name': 'Post'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'posts'", 'to': u"orm['blog.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'extra_footer_paths': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'footered_blog_posts'", 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            'extra_header_paths': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'headered_blog_posts'", 'symmetrical': 'False', 'to': u"orm['base.ExtraPath']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '7'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'posts'", 'symmetrical': 'False', 'to': u"orm['blog.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blog.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['blog']