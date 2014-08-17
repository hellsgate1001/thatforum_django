from django import forms
from django.contrib.auth import get_user_model


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


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
