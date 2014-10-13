from django.conf.urls import patterns, include, url

from .views import (UserList, UserDetail, UserCreate, UserUpdate, UserLogin,
    UserProfile)

forumuser_patterns = patterns('',
    url(r'^$', UserList.as_view(), name='list'),
    url(r'add/$', UserCreate.as_view(), name='create'),
    url(r'^(?P<pk>[-\d]+)/$', UserDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[-\d]+)/edit/$', UserUpdate.as_view(), name='edit'),
    url(r'^my_account/$', UserProfile.as_view(), name='my_account'),

    url(r'^login/$', UserLogin.as_view(), name='login'),
)

urlpatterns = patterns('',
    url(r'^',include(forumuser_patterns, namespace='user'))
)
