from django import forms
from django.contrib import auth


class BootstrapTextInput(forms.TextInput):
    def __init__(self, attrs={}, *args, **kwargs):
        attrs = {**attrs,
                 'class': 'form-control'}
        forms.TextInput.__init__(self, attrs=attrs)


class BootstrapPasswordInput(BootstrapTextInput):
    def __init__(self, attrs={}, *args, **kwargs):
        attrs = {**attrs,
                 'type': 'password'}
        BootstrapTextInput.__init__(self, attrs=attrs)


class SignInForm(forms.Form):
    user_name = forms.CharField(max_length=20, label='Login', widget=BootstrapTextInput)
    password = forms.CharField(label='Password', widget=BootstrapPasswordInput)

    def clean(self):
        self._user = auth.authenticate(username=self.cleaned_data['user_name'], password=self.cleaned_data['password'])
        if not self._user:
            raise forms.ValidationError('Invalid login or password')

    def auth(self):
        if not self._user:
            self.clean()
        return self._user

    _user = None
