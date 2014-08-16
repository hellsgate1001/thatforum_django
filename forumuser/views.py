from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import UserForm


class UserViewMixin(object):
    def __init__(self, *args, **kwargs):
        self.model = get_user_model()
        super(UserViewMixin, self).__init__(*args, **kwargs)


class UserList(UserViewMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATE_BY


class UserDetail(UserViewMixin, DetailView):
    """
    View for displaying user details
    """


class UserUpdate(UserViewMixin, UpdateView):
    """
    Edit the details for an existing user
    """
    form_class = UserForm

class UserCreate(UserViewMixin, CreateView):
    """
    Create a new user
    """
    form_class = UserForm

    def get_success_url(self, *args, **kwargs):
        return self.object.get_absolute_url()
