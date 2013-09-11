# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Interface'
        db.create_table(u'network_interface', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_new', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('_changed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('type', self.gf('django.db.models.fields.CharField')(default='ethernet', max_length=10)),
            ('mode', self.gf('django.db.models.fields.CharField')(default='notset', max_length=10)),
            ('address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
            ('netmask', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
        ))
        db.send_create_signal(u'network', ['Interface'])


    def backwards(self, orm):
        # Deleting model 'Interface'
        db.delete_table(u'network_interface')


    models = {
        u'network.interface': {
            'Meta': {'object_name': 'Interface'},
            '_changed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            '_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            '_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'default': "'notset'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'netmask': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'ethernet'", 'max_length': '10'})
        }
    }

    complete_apps = ['network']