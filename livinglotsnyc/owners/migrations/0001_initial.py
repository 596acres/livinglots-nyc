# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Owner'
        db.create_table(u'owners_owner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('owner_type', self.gf('django.db.models.fields.CharField')(default='private', max_length=20)),
        ))
        db.send_create_signal(u'owners', ['Owner'])

        # Adding M2M table for field aliases on 'Owner'
        db.create_table(u'owners_owner_aliases', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('owner', models.ForeignKey(orm[u'owners.owner'], null=False)),
            ('alias', models.ForeignKey(orm[u'livinglots_owners.alias'], null=False))
        ))
        db.create_unique(u'owners_owner_aliases', ['owner_id', 'alias_id'])


    def backwards(self, orm):
        # Deleting model 'Owner'
        db.delete_table(u'owners_owner')

        # Removing M2M table for field aliases on 'Owner'
        db.delete_table('owners_owner_aliases')


    models = {
        u'livinglots_owners.alias': {
            'Meta': {'object_name': 'Alias'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'owners.owner': {
            'Meta': {'object_name': 'Owner'},
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['livinglots_owners.Alias']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'owner_type': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '20'})
        }
    }

    complete_apps = ['owners']