from django.conf.urls import patterns, include, url

from .views import ForumHome


forum_patterns = patterns('',
    url(r'^$', ForumHome.as_view(), name='list'),
)

urlpatterns = patterns('',
    url(r'^',include(forum_patterns, namespace='forum'))
)
