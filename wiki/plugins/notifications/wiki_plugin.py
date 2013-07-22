from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from django.conf.urls import patterns, url

import settings, views


class NotifyPlugin(BasePlugin):
    slug = settings.SLUG

    urlpatterns = {
        'root': patterns('',
            url('^watch/$', views.WatchView.as_view(), name='watch'),
            url('^stop_watching/$', views.StopWatchingView.as_view(), name='stop_watching'),
        )
    }
 
    def watching_status(self, article, viewer):
        import wiki.plugins.notifications.models as M
        watch_status = M.ArticleSubscription.objects.filter(article=article, viewer=viewer).count() > 0
        return watch_status

registry.register(NotifyPlugin)
