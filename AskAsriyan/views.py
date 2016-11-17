from django.http.response import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import Http404, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
import random


def base_decorator(func):
    def decorator(request, *args, **kwargs):
        class _tag:
            def __init__(self, name, weight):
                self.name = name
                self.weight = weight

        tags = [_tag(''.join([chr(random.randint(ord('A'), ord('z'))) for j in
                              range(0, random.randint(5, 10))]), random.randint(10, 25)) for i in
                range(random.randint(15, 35))]

        return func(request, tags=tags, user=auth.get_user(request), **kwargs)

    return decorator


@base_decorator
def index_page_view(request, *args, **kwargs):
    return redirect('/articles/1')


@base_decorator
def article_list_page_view(request, page=1, *args, **kwargs):
    page = int(page)
    articles = Paginator(models.Article.objects.all(), 10)
    if page > articles.num_pages:
        return redirect('/')
    return render_to_response('index.html', {'articles': articles.page(page), 'is_preview': True, **kwargs})


@base_decorator
def sign_in_page_view(request, *args, **kwargs):
    return render_to_response('sign_in.html', kwargs)


@base_decorator
def sign_up_page_view(request, *args, **kwargs):
    return render_to_response('sign_up.html', kwargs)


def login_view(request, *args, **kwargs):
    if request.POST:
        form = forms.SignInForm(request.POST)
        if form.is_valid():
            auth.login(request, form.auth())
            return redirect('/')
    else:
        form = forms.SignInForm()
    return sign_in_page_view(request, form=form, *args, **kwargs)


def logout_view(request, *args, **kwargs):
    auth.logout(request)
    return redirect('/')


def register_view(request, *args, **kwargs):
    if request.POST:
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/sign_in/')
    else:
        form = forms.SignUpForm()
    return sign_up_page_view(request, form=form, *args, **kwargs)


@base_decorator
def article_view(request, article_id, *args, **kwargs):
    try:
        article_id = int(article_id)
        article = models.Article.objects.get(id=article_id)
    except Exception:
        raise Http404()
    finally:
        pass

    return render_to_response('article.html', {'article': article, 'is_preview': False, **kwargs})


@base_decorator
def article_add_page_view(request, *args, **kwargs):
    return render_to_response('ask.html', kwargs)


@login_required
def article_add_view(request, *args, **kwargs):
    if request.POST:
        form = forms.ArticleAddForm(request.user, request.POST)
        if form.is_valid():
            return redirect(form.save().get_url())

    else:
        form = forms.ArticleAddForm()
    return article_add_page_view(request, form=form, *args, **kwargs)
