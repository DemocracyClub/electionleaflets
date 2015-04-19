# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Party.show_on_add_page'
        db.add_column(u'party', 'show_on_add_page', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Party.show_on_add_page'
        db.delete_column(u'party', 'show_on_add_page')


    models = {
        'core.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'country'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '240'})
        },
        'parties.party': {
            'Meta': {'object_name': 'Party', 'db_table': "u'party'"},
            'colour': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Country']"}),
            'force_top': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo_file': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'major': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'popular': ('django.db.models.fields.IntegerField', [], {}),
            'show_on_add_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'twitter_account': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'url_id': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'})
        }
    }

    complete_apps = ['parties']
