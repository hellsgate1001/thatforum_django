from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    FormView
    )
from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from thatforum.mixins import RequestForFormMixIn

from .forms import LoginForm, UserForm, ChangePasswordForm


class UserLogin(FormView):
    form_class = AuthenticationForm
    template_name = 'forumuser/forumuser_form.html'

    def form_valid(self, form):
        return login(self.request, template_name='users/login.html')


class UserViewMixin(object):
    def __init__(self, *args, **kwargs):
        self.model = get_user_model()
        super(UserViewMixin, self).__init__(*args, **kwargs)


class UserList(LoginRequiredMixin, UserViewMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATE_BY


class UserDetail(LoginRequiredMixin, UserViewMixin, DetailView):
    """
    View for displaying user details
    """


class UserUpdate(LoginRequiredMixin, PermissionRequiredMixin,
    UserViewMixin, UpdateView):
    """
    Edit the details for an existing user
    """
    form_class = UserForm
    permission_required = 'forumuser.change_user'


class UserCreate(LoginRequiredMixin, PermissionRequiredMixin,
    UserViewMixin, CreateView):
    """
    Create a new user
    """
    form_class = UserForm
    permission_required = 'forumuser.add_user'

    def get_success_url(self, *args, **kwargs):
        return self.object.get_absolute_url()


class UserProfile(LoginRequiredMixin, UserViewMixin, UpdateView):
    """
    Allow a user to update their own details and profile
    """
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdatePassword(
    LoginRequiredMixin,
    UserViewMixin,
    RequestForFormMixIn,
    UpdateView
):
    form_class = ChangePasswordForm

    def get_success_url(self):
        return reverse('user:my_account')
