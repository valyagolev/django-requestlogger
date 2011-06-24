# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Request'
        db.create_table('requestlogger_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('response_time', self.gf('django.db.models.fields.FloatField')()),
            ('status_code', self.gf('django.db.models.fields.IntegerField')()),
            ('exception_class', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('exception_message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('requestlogger', ['Request'])


    def backwards(self, orm):
        
        # Deleting model 'Request'
        db.delete_table('requestlogger_request')


    models = {
        'requestlogger.request': {
            'Meta': {'object_name': 'Request'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'exception_class': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exception_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'response_time': ('django.db.models.fields.FloatField', [], {}),
            'status_code': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['requestlogger']
