from django.conf.urls import patterns, include, url

from .views import UserList, UserDetail, UserCreate, UserUpdate


forumuser_patterns = patterns('',
    url(r'^$', UserList.as_view(), name='list'),
    url(r'', UserCreate.as_view(), name='create'),
    url(r'^(?P<pk>[-\d]+)/$', UserDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[-\d]+)/edit/$', UserUpdate.as_view(), name='edit'),
)

urlpatterns = patterns('',
    url(r'^',include(forumuser_patterns, namespace='user'))
)
