# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.attachments import views
from wiki.plugins.attachments import models
from wiki.plugins.attachments import settings
from wiki.plugins.attachments.markdown_extensions import AttachmentExtension

class AttachmentPlugin(BasePlugin):
    
    slug = settings.SLUG
    urlpatterns = {
        'article': patterns('',
            url(r'^$', views.AttachmentView.as_view(), name='attachments_index'),
            url(r'^search/$', views.AttachmentSearchView.as_view(), name='attachments_search'),
            url(r'^add/(?P<attachment_id>\d+)/$', views.AttachmentAddView.as_view(), name='attachments_add'),
            url(r'^replace/(?P<attachment_id>\d+)/$', views.AttachmentReplaceView.as_view(), name='attachments_replace'),
            url(r'^history/(?P<attachment_id>\d+)/$', views.AttachmentHistoryView.as_view(), name='attachments_history'),
            url(r'^download/(?P<attachment_id>\d+)/$', views.AttachmentDownloadView.as_view(), name='attachments_download'),
            url(r'^delete/(?P<attachment_id>\d+)/$', views.AttachmentDeleteView.as_view(), name='attachments_delete'),
            url(r'^download/(?P<attachment_id>\d+)/revision/(?P<revision_id>\d+)/$', views.AttachmentDownloadView.as_view(), name='attachments_download'),
            url(r'^change/(?P<attachment_id>\d+)/revision/(?P<revision_id>\d+)/$', views.AttachmentChangeRevisionView.as_view(), name='attachments_revision_change'),
        )
    }
    
    article_tab = (_(u'Attachments'), "icon-file")
    article_view = views.AttachmentView().dispatch
    
    markdown_extensions = [AttachmentExtension()]
    
    def __init__(self):
        #print "I WAS LOADED!"
        pass
    
registry.register(AttachmentPlugin)

