from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

# from .views import HomeView
from .views import (ForumHome, ForumCategoryHome, ForumThreadHome,
    ForumThreadCreateView, ForumThreadReply)

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'thatforum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^office/', include(admin.site.urls)),
    url(r'^users/', include('forumuser.urls')),
    # url(r'^forum/', include('forum.urls')),

    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('home')},
        name='logout'
    ),

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

    # url(r'^$', HomeView.as_view(), name='home'),
)
