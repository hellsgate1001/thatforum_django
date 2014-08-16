from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView


class UserViewMixin(object):
    def __init__(self, *args, **kwargs):
        self.model = get_user_model()
        super(UserViewMixin, self).__init__(*args, **kwargs)


class UserList(UserViewMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATE_BY


class UserDetail(UserViewMixin, DetailView):
    pass


class UserUpdate(UserViewMixin, UpdateView):
    pass


class UserCreate(UserViewMixin, CreateView):
    pass
