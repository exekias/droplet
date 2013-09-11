# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ModuleInfo'
        db.create_table(u'core_moduleinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_new', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('_changed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('changed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['ModuleInfo'])


    def backwards(self, orm):
        # Deleting model 'ModuleInfo'
        db.delete_table(u'core_moduleinfo')


    models = {
        u'core.moduleinfo': {
            'Meta': {'object_name': 'ModuleInfo'},
            '_changed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'changed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['core']