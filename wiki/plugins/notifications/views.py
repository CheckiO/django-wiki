from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from django.utils.decorators import method_decorator
from wiki.views.mixins import ArticleMixin
from wiki.decorators import get_article


class WatchView(ArticleMixin, RedirectView):
    permanent = False

    @method_decorator(get_article(can_read=True))
    def dispatch(self, request, article, *args, **kwargs):
        self.article = article
        self.subscribe(request.user)
        return super(WatchView, self).dispatch(request, article, *args, **kwargs)

    def get_redirect_url(self):
        url = reverse_lazy('wiki:get', kwargs={'article_id': self.article.id})
        return url

    def subscribe(self, user):
        import wiki.plugins.notifications.models as M
        M.ArticleSubscription.objects.get_or_create(article=self.article, viewer=user)


class StopWatchingView(WatchView):
    def subscribe(self, user):
        import wiki.plugins.notifications.models as M
        M.ArticleSubscription.objects.filter(article=self.article, viewer=user).delete()
