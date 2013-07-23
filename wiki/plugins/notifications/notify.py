from notifies.base import notifications, NotificationBase

NOTIFICATION_ARTICLE_UPDATED = 'notification_article_updated'
NOTIFICATION_ARTICLE_DELETED = 'notification_article_deleted'

class NotificationArticleUpdated(NotificationBase):
    template_text = "%(actor_user)s updated article %(action_object)s"
    notification_type = NOTIFICATION_ARTICLE_UPDATED
    verbose_name = "Article updated"
    verbose_description = "Someone updated article that you are watching"
notifications.register(NotificationArticleUpdated)

class NotificationArticleDeleted(NotificationBase):
    template_text = "%(actor_user)s deleted article %(action_object)s"
    notification_type = NOTIFICATION_ARTICLE_DELETED
    verbose_name = "Article deleted"
    verbose_description = "Someone deleted article that you are watching"
notifications.register(NotificationArticleDeleted)

