import datetime

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
    tags = forms.CharField(label='Tags', widget=BootstrapStringInput, required=False)

    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            user = models.Article.objects.get(article_title=title)
        except models.Article.DoesNotExist:
            return title
        raise forms.ValidationError('Question "%s" is already exist.' % title)

    def clean_tags(self):
        return self.cleaned_data['tags']

    def save(self):
        article_title = self.cleaned_data['title']
        article_body = self.cleaned_data['text']
        article_date = datetime.datetime.now()
        article_rating = 0
        article_author = self._user

        article = models.Article.objects.create(article_title=article_title, article_body=article_body,
                                                article_date=article_date, article_rating=article_rating,
                                                article_author=article_author)
        article.save()
        return article


class CommentAddForm(forms.Form):
    text = forms.CharField(widget=BootstrapTextInput(attrs={'placeholder': 'Type your comment here...'}))
    article_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, user=None, *args, **kwargs):
        self._user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text or not len(text):
            raise forms.ValidationError('This field is required.')
        return text

    def clean_article_id(self):
        id = self.cleaned_data['article_id']
        if models.Article.objects.get(id=id):
            return id
        raise forms.ValidationError('Article does not exist.')

    def save(self):
        comment_body = self.cleaned_data['text']
        comment_date = datetime.datetime.now()
        comment_rating = 0
        comment_author = self._user
        comment_article_id = self.cleaned_data['article_id']
        comment = models.Comment.objects.create(comment_author=comment_author, comment_body=comment_body,
                                                comment_rating=comment_rating, comment_date=comment_date,
                                                comment_article_id=comment_article_id)

        comment.save()
        return comment


class SettingsForm(forms.Form):
    login = forms.CharField(max_length=20, label='Login', widget=BootstrapStringInput)
    email = forms.CharField(max_length=255, label='E-mail', widget=BootstrapEmailInput)
    nick = forms.CharField(max_length=20, label='Nick', widget=BootstrapStringInput)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        forms.Form.__init__(self, initial={'login': user.username, 'email': user.email, 'nick': user.first_name}, *args,
                            **kwargs)

    def clean_login(self):
        username = self.cleaned_data['login']
        if username == self._user.username:
            return username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == self._user.email:
            return email
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('E-mail "%s" is already in use.' % email)

    def save(self):
        self._user.username = self.cleaned_data['login']
        self._user.email = self.cleaned_data['email']
        self._user.first_name = self.cleaned_data['nick']

        self._user.save()
