# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Request.view_module'
        db.add_column('requestlogger_request', 'view_module', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Request.view_func'
        db.add_column('requestlogger_request', 'view_func', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Request.view_module'
        db.delete_column('requestlogger_request', 'view_module')

        # Deleting field 'Request.view_func'
        db.delete_column('requestlogger_request', 'view_func')


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
            'status_code': ('django.db.models.fields.IntegerField', [], {}),
            'view_func': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'view_module': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['requestlogger']
