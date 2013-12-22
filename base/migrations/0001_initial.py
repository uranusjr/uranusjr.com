# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExtraPath'
        db.create_table(u'base_extrapath', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('path', self.gf('django.db.models.fields.FilePathField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'base', ['ExtraPath'])


    def backwards(self, orm):
        # Deleting model 'ExtraPath'
        db.delete_table(u'base_extrapath')


    models = {
        u'base.extrapath': {
            'Meta': {'object_name': 'ExtraPath'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'path': ('django.db.models.fields.FilePathField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['base']