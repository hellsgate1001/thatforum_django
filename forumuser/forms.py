from django import forms
from django.contrib.auth import get_user_model

from thatforum.forms import ThatForumBaseForm


class LoginForm(forms.ModelForm):
    """
    Form for users to log in to the  site
    """
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class UserForm(ThatForumBaseForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)


class PasswordFieldsMixin(object):
    password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=128
    )
    password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=128
    )

    def clean(self):
        cleaned_data = super(PasswordFieldsMixin, self).clean()
        pw1 = cleaned_data.get('password1', '')
        pw2 = cleaned_data.get('password2', '')
        if pw1 != '' and pw2 != '' and pw1 != pw2:
            raise forms.ValidationError('The passwords do not match')
        return cleaned_data


class ChangePasswordForm(ThatForumBaseForm):
    old_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput,
        max_length=128
    )
    password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=128
    )
    password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=128
    )

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        cleaned_data = self.cleaned_data['old_password']
        if not self.request.user.check_password(cleaned_data):
            raise forms.ValidationError('The password entered is incorrect')
        return cleaned_data

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        pw1 = cleaned_data.get('password1', '')
        pw2 = cleaned_data.get('password2', '')
        if pw1 != '' and pw2 != '' and pw1 != pw2:
            raise forms.ValidationError('The passwords do not match')
        return cleaned_data

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'password1', 'password2')


class SignupForm(PasswordFieldsMixin, ThatForumBaseForm):
    password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=128
    )
    password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=128
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        pw1 = cleaned_data.get('password1', '')
        pw2 = cleaned_data.get('password2', '')
        if pw1 != '' and pw2 != '' and pw1 != pw2:
            raise forms.ValidationError('The passwords do not match')
        return cleaned_data

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')
