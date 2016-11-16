from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from . import models


class BootstrapStringInput(forms.TextInput):
    def __init__(self, attrs={}, *args, **kwargs):
        attrs = {**attrs,
                 'class': 'form-control'}
        forms.TextInput.__init__(self, attrs=attrs)


class BootstrapPasswordInput(BootstrapStringInput):
    def __init__(self, attrs={}, *args, **kwargs):
        attrs = {**attrs,
                 'type': 'password'}
        BootstrapStringInput.__init__(self, attrs=attrs)


class BootstrapEmailInput(BootstrapStringInput):
    def __init__(self, attrs={}, *args, **kwargs):
        attrs = {**attrs,
                 'type': 'email'}
        BootstrapStringInput.__init__(self, attrs=attrs)


def BootstrapTextInput(attrs={}, *args, **kwargs):
    attrs = {**attrs,
             'class': 'form-control',
             'rows': '5',
             'style': 'resize:vertical;'}
    return forms.Textarea(attrs=attrs, **kwargs)


class SignInForm(forms.Form):
    user_name = forms.CharField(max_length=20, label='Login', widget=BootstrapStringInput)
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


class SignUpForm(forms.Form):
    login = forms.CharField(max_length=20, label='Login', widget=BootstrapStringInput)
    email = forms.CharField(max_length=255, label='E-mail', widget=BootstrapEmailInput)
    nick = forms.CharField(max_length=20, label='Nick', widget=BootstrapStringInput)
    password = forms.CharField(max_length=20, min_length=4, label='Password', widget=BootstrapPasswordInput)
    password_repeat = forms.CharField(max_length=20, min_length=4, label='Repeat', widget=BootstrapPasswordInput)

    def clean_login(self):
        username = self.cleaned_data['login']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('E-mail "%s" is already in use.' % email)

    def clean_password_repeat(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_repeat']:
            raise forms.ValidationError('Passwords is not equal.')

    def save(self):
        self.user = User.objects.create_user(self.cleaned_data['login'], self.cleaned_data['email'],
                                             self.cleaned_data['password'], first_name=self.cleaned_data['nick'])


class ArticleAddForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=3, widget=BootstrapStringInput)
    text = forms.CharField(label='Text', widget=BootstrapTextInput())

    def __init__(self, user, *args, **kwargs):
        self._user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['article_title']
        try:
            user = models.Article.objects.get(article_title=title)
        except User.DoesNotExist:
            return title
        raise forms.ValidationError('Question "%s" is already exist.' % title)
