from django.conf.urls import patterns, include, url

from .views import (ForumHome, ForumCategoryHome, ForumThreadHome,
    ForumThreadCreateView, ForumThreadReply)


forum_patterns = patterns('',
    url(r'^$', ForumHome.as_view(), name='list'),
    url(r'^category/(?P<slug>[-\w]+)/new/$', ForumThreadCreateView.as_view(),
        name='add_thread'),
    url(r'^category/(?P<slug>[-\w]+)/$', ForumCategoryHome.as_view(),
        name='category_home'),
    url(r'^thread/(?P<slug>[-\w]+)/$', ForumThreadHome.as_view(),
        name='thread_home'),
    url(r'^thread/(?P<slug>[-\w]+)/reply/(?P<quote_pk>[-\d]+)/$', ForumThreadReply.as_view(),
        name='thread_reply_quote'),
    url(r'^thread/(?P<slug>[-\w]+)/reply/$', ForumThreadReply.as_view(),
        name='thread_reply'),
)

urlpatterns = patterns('',
    url(r'^', include(forum_patterns, namespace='forum'))
)
