from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

from .views import HomeView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'thatforum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^office/', include(admin.site.urls)),
    url(r'^users/', include('forumuser.urls')),
    url(r'^forum/', include('forum.urls')),

    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('home')},
        name='logout'
    ),

    url(r'^$', HomeView.as_view(), name='home'),
)
