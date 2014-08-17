from django.conf.urls import patterns, include, url

forum_urlpatterns = patterns('',
    url(r'^$', ForumHome.as_view(), name='home'),
)

urlpatterns = patterns('',
    include(forum_urlpatterns, namespace='forum')
)
