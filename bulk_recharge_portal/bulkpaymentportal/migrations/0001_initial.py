# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Credits'
        db.create_table(u'bulkpaymentportal_credits', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('account_balance', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('account_type', self.gf('django.db.models.fields.CharField')(default='Prepaid', max_length=8)),
        ))
        db.send_create_signal(u'bulkpaymentportal', ['Credits'])

        # Adding model 'AccountPayment'
        db.create_table(u'bulkpaymentportal_accountpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('previous_balance', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('after_balance', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('recharge_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('date_of_recharge', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'bulkpaymentportal', ['AccountPayment'])

        # Adding model 'User_account'
        db.create_table(u'bulkpaymentportal_user_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('balance', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('recharges', self.gf('django.db.models.fields.BigIntegerField')(max_length=999999999999999)),
            ('date_of_recharge', self.gf('django.db.models.fields.DateField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'bulkpaymentportal', ['User_account'])

        # Adding model 'Recharge'
        db.create_table(u'bulkpaymentportal_recharge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recharged_number', self.gf('django.db.models.fields.BigIntegerField')(max_length=999999999999999)),
            ('recharge_value', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('date_of_reacharge', self.gf('django.db.models.fields.DateField')()),
            ('triggered_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'bulkpaymentportal', ['Recharge'])

        # Adding model 'Countries'
        db.create_table(u'bulkpaymentportal_countries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country_iso_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('country_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'bulkpaymentportal', ['Countries'])

        # Adding model 'PaymentGateways'
        db.create_table(u'bulkpaymentportal_paymentgateways', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('supported_country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulkpaymentportal.Countries'])),
        ))
        db.send_create_signal(u'bulkpaymentportal', ['PaymentGateways'])

        # Adding model 'TelecomNetwork'
        db.create_table(u'bulkpaymentportal_telecomnetwork', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('network', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulkpaymentportal.Countries'])),
        ))
        db.send_create_signal(u'bulkpaymentportal', ['TelecomNetwork'])

        # Adding model 'RechargeProviders'
        db.create_table(u'bulkpaymentportal_rechargeproviders', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('supported_network_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulkpaymentportal.TelecomNetwork'])),
        ))
        db.send_create_signal(u'bulkpaymentportal', ['RechargeProviders'])

        # Adding model 'NumberGroups'
        db.create_table(u'bulkpaymentportal_numbergroups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_group_owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('saved_numbers', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'bulkpaymentportal', ['NumberGroups'])


    def backwards(self, orm):
        # Deleting model 'Credits'
        db.delete_table(u'bulkpaymentportal_credits')

        # Deleting model 'AccountPayment'
        db.delete_table(u'bulkpaymentportal_accountpayment')

        # Deleting model 'User_account'
        db.delete_table(u'bulkpaymentportal_user_account')

        # Deleting model 'Recharge'
        db.delete_table(u'bulkpaymentportal_recharge')

        # Deleting model 'Countries'
        db.delete_table(u'bulkpaymentportal_countries')

        # Deleting model 'PaymentGateways'
        db.delete_table(u'bulkpaymentportal_paymentgateways')

        # Deleting model 'TelecomNetwork'
        db.delete_table(u'bulkpaymentportal_telecomnetwork')

        # Deleting model 'RechargeProviders'
        db.delete_table(u'bulkpaymentportal_rechargeproviders')

        # Deleting model 'NumberGroups'
        db.delete_table(u'bulkpaymentportal_numbergroups')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bulkpaymentportal.accountpayment': {
            'Meta': {'object_name': 'AccountPayment'},
            'after_balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'date_of_recharge': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'recharge_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bulkpaymentportal.countries': {
            'Meta': {'object_name': 'Countries'},
            'country_iso_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'country_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'bulkpaymentportal.credits': {
            'Meta': {'object_name': 'Credits'},
            'account_balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'account_type': ('django.db.models.fields.CharField', [], {'default': "'Prepaid'", 'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bulkpaymentportal.numbergroups': {
            'Meta': {'object_name': 'NumberGroups'},
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'saved_numbers': ('django.db.models.fields.TextField', [], {}),
            'user_group_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bulkpaymentportal.paymentgateways': {
            'Meta': {'object_name': 'PaymentGateways'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'supported_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulkpaymentportal.Countries']"})
        },
        u'bulkpaymentportal.recharge': {
            'Meta': {'object_name': 'Recharge'},
            'date_of_reacharge': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recharge_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'recharged_number': ('django.db.models.fields.BigIntegerField', [], {'max_length': '999999999999999'}),
            'triggered_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bulkpaymentportal.rechargeproviders': {
            'Meta': {'object_name': 'RechargeProviders'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'supported_network_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulkpaymentportal.TelecomNetwork']"})
        },
        u'bulkpaymentportal.telecomnetwork': {
            'Meta': {'object_name': 'TelecomNetwork'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulkpaymentportal.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'bulkpaymentportal.user_account': {
            'Meta': {'object_name': 'User_account'},
            'balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_of_recharge': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recharges': ('django.db.models.fields.BigIntegerField', [], {'max_length': '999999999999999'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bulkpaymentportal']