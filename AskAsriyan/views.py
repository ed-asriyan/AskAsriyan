from django.http.response import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import Http404, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
import random


def base_decorator(func):
    def decorator(request, *args, **kwargs):
        tags = models.Tag.objects.get_popular()

        min_height = min(tags, key=lambda x: x.article_count).article_count
        max_height = max(tags, key=lambda x: x.article_count).article_count

        for tag in tags:
            tag.tag_weight = (tag.get_articles_count() - min_height) // (max_height - min_height) * 8 + 10

        return func(request, tags=tags, user=auth.get_user(request), **kwargs)

    return decorator


def pagination(request, html_page, objects, object_name, objects_count, *args, **kwargs):
    paginator = Paginator(objects, objects_count)
    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    kwargs[object_name] = objects
    kwargs['pagination_list'] = objects

    return render_to_response(html_page, {**kwargs})


@base_decorator
def index_page_view(request, *args, **kwargs):
    return redirect('/articles?page=1')


@base_decorator
def article_list_page_view(request, *args, **kwargs):
    if request.GET.get('tag'):
        articles = models.Article.objects.get_by_tag(request.GET.get('tag'))
    else:
        articles = models.Article.objects.all()
    return pagination(request, 'lists/article_list.html', articles, 'articles', 10, *args, **kwargs)


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
    article = models.Article.objects.get(id=article_id)
    if request.POST:
        form = forms.CommentAddForm(request.user, request.POST)
        if form.is_valid():
            return redirect(form.save().get_url())
    else:
        form = forms.CommentAddForm(initial={'article_id': article_id})

    comments = article.get_comments()
    return pagination(request, 'article.html', comments, 'comments', 5, article=article, is_preview=False, form=form,
                      *args, **kwargs)


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


@base_decorator
def profile_settings_view(request, *args, **kwargs):
    if request.POST:
        form = forms.SettingsForm(request.user, request.POST)
        if form.is_valid():
            form.save()
    else:
        form = forms.SettingsForm(request.user)
    return render_to_response('profile_settings.html', {'form': form, **kwargs})
