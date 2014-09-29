from django.conf.urls import patterns, include, url

from .views import ForumHome, ForumCategoryHome, ForumThreadHome


forum_patterns = patterns('',
    url(r'^$', ForumHome.as_view(), name='list'),
    url(r'^category/(?P<slug>[-\w]+)/$', ForumCategoryHome.as_view(),
        name='category_home'),
    url(r'^thread/(?P<slug>[-\w]+)/$', ForumThreadHome.as_view(),
        name='thread_home'),
)

urlpatterns = patterns('',
    url(r'^', include(forum_patterns, namespace='forum'))
)
