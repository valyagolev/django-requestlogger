# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'View'
        db.create_table('requestlogger_view', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('func', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('requestlogger', ['View'])

        # Adding unique constraint on 'View', fields ['module', 'func']
        db.create_unique('requestlogger_view', ['module', 'func'])

        # Deleting field 'Request.view_module'
        db.delete_column('requestlogger_request', 'view_module')

        # Deleting field 'Request.view_func'
        db.delete_column('requestlogger_request', 'view_func')

        # Adding field 'Request.view'
        db.add_column('requestlogger_request', 'view', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['requestlogger.View'], null=True), keep_default=False)


    def backwards(self, orm):
        
        # Removing unique constraint on 'View', fields ['module', 'func']
        db.delete_unique('requestlogger_view', ['module', 'func'])

        # Deleting model 'View'
        db.delete_table('requestlogger_view')

        # Adding field 'Request.view_module'
        db.add_column('requestlogger_request', 'view_module', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Request.view_func'
        db.add_column('requestlogger_request', 'view_func', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Deleting field 'Request.view'
        db.delete_column('requestlogger_request', 'view_id')


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
            'view': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['requestlogger.View']", 'null': 'True'})
        },
        'requestlogger.view': {
            'Meta': {'unique_together': "[('module', 'func')]", 'object_name': 'View'},
            'func': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['requestlogger']
