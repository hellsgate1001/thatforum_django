from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login as auth_login
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

from .forms import LoginForm, UserForm, ChangePasswordForm, SignupForm


class UserLogin(FormView):
    form_class = AuthenticationForm
    template_name = 'forumuser/forumuser_form.html'

    def form_valid(self, form):
        return login(self.request, template_name='users/login.html')

    def get_context_data(self, **kwargs):
        context = super(UserLogin, self).get_context_data(**kwargs)
        context['hide_edit_password'] = True
        return context


class UserViewMixin(object):
    def __init__(self, *args, **kwargs):
        self.model = get_user_model()
        super(UserViewMixin, self).__init__(*args, **kwargs)


class UserSignupView(UserViewMixin, RequestForFormMixIn, CreateView):
    form_class = SignupForm

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET' and 'HTTP_REFERER' in request.META.keys():
            request.session['success_url'] = request.META['HTTP_REFERER']
            request.session.save()
        return super(UserSignupView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserSignupView, self).get_context_data(**kwargs)
        context['hide_edit_password'] = True
        return context

    def get_success_url(self):
        if 'success_url' in self.request.META.keys():
            success_url = self.request.session['success_url']
            del(self.request.session['success_url'])
        else:
            success_url = self.object.get_absolute_url()
        return success_url

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data.get('password1'))
        form.instance.username = form.instance.email
        form.instance.save()
        login_user = authenticate(
            username=form.instance.username,
            password=form.cleaned_data.get('password1')
        )
        if login_user is not None:
            auth_login(self.request, login_user)
        return super(UserSignupView, self).form_valid(form)


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


class UserProfile(
    LoginRequiredMixin,
    UserViewMixin,
    RequestForFormMixIn,
    UpdateView
):
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
    template_name = 'forumuser/changepassword_form.html'

    def get_success_url(self):
        return reverse('user:my_account')

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data.get('password1'))
        return super(UserUpdatePassword, self).form_valid(form)
