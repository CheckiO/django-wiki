# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.db import models

from wiki import models as wiki_models
from wiki.models.pluginbase import ArticlePlugin
from wiki.core.plugins import registry
from wiki.plugins.notifications import settings
from wiki.plugins.notifications.util import get_title

from wiki.plugins.notifications.notify import NOTIFICATION_ARTICLE_UPDATED, NOTIFICATION_ARTICLE_DELETED
from notifies.models import Notification
from django.contrib.auth.models import User


class ArticleSubscription(models.Model):
    article = models.ForeignKey(wiki_models.Article, related_name='viewers', on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)


def default_url(article, urlpath=None):
    try:
        if not urlpath:
            urlpath = wiki_models.URLPath.objects.get(articles=article)
        url = reverse('wiki:get', kwargs={'path': urlpath.path})
    except wiki_models.URLPath.DoesNotExist:
        url = reverse('wiki:get', kwargs={'article_id': article.id})
    return url

def post_article_revision_save(**kwargs):
    instance = kwargs['instance']
    article = instance.article
    if kwargs.get('created', False):
        if instance.deleted or instance.previous_revision:
            users = [av.viewer for av in article.viewers.all()]
        else:
            users = User.objects.all()

        for user in users:
            if instance.user == user:
                continue
            if instance.deleted:
                Notification.objects.send(user, instance.user, NOTIFICATION_ARTICLE_DELETED, article)
            elif instance.previous_revision:
                Notification.objects.send(user, instance.user, NOTIFICATION_ARTICLE_UPDATED, article)

# Whenever a new revision is created, we notifý users that an article
# was edited
signals.post_save.connect(post_article_revision_save, sender=wiki_models.ArticleRevision,)
