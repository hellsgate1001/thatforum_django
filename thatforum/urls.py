from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'thatforum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^office/', include(admin.site.urls)),
    url(r'^users/', include('forumuser.urls')),
    url(r'^forum/', include('forum.urls')),
)
