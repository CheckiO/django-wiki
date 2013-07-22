# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)

class Migration(SchemaMigration):

    def forwards(self, orm):
        from notification.models import NoticeType
        from wiki.plugins.notifications.notify import NOTIFICATION_ARTICLE_UPDATED, NOTIFICATION_ARTICLE_DELETED

        try:
            new_notification_type = NoticeType.objects.get(label=NOTIFICATION_ARTICLE_UPDATED)
        except NoticeType.DoesNotExist:
            new_notification_type = NoticeType.objects.create(
                label = NOTIFICATION_ARTICLE_UPDATED,
                display = 'Updated article',
                description = 'Someone updated article that you are watching',
                default = '2'
            )

        try:
            new_notification_type = NoticeType.objects.get(label=NOTIFICATION_ARTICLE_DELETED)
        except NoticeType.DoesNotExist:
            new_notification_type = NoticeType.objects.create(
                label = NOTIFICATION_ARTICLE_DELETED,
                display = 'Deleted article',
                description = 'Someone deleted article that you are watching',
                default = '2'
            )

        # Adding model 'ArticleSubscription'
        db.create_table('notifications_articlesubscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(related_name='viewers', to=orm['wiki.Article'])),
            ('viewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('notifications', ['ArticleSubscription'])



    def backwards(self, orm):
        # Deleting model 'ArticleSubscription'
        db.delete_table('notifications_articlesubscription')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        user_model_label: {
            'Meta': {'object_name': User.__name__, 'db_table': "'%s'" % User._meta.db_table},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notifications.articlesubscription': {
            'Meta': {'object_name': 'ArticleSubscription'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewers'", 'to': "orm['wiki.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'viewer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'wiki.article': {
            'Meta': {'object_name': 'Article'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_revision': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'current_set'", 'unique': 'True', 'null': 'True', 'to': "orm['wiki.ArticleRevision']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'group_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'group_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'other_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'other_write': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_articles'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"})
        },
        'wiki.articlerevision': {
            'Meta': {'ordering': "('created',)", 'unique_together': "(('article', 'revision_number'),)", 'object_name': 'ArticleRevision'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Article']"}),
            'automatic_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.ArticleRevision']", 'null': 'True', 'blank': 'True'}),
            'revision_number': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'user_message': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['notifications']
