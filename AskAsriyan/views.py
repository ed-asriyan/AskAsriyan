from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from . import models
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

        return func(request, tags=tags, **kwargs)

    return decorator


@base_decorator
def sign_in_view(request, *args, **kwargs):
    return render_to_response('sign_in.html', kwargs)


@base_decorator
def sign_up_view(request, *args, **kwargs):
    return render_to_response('sign_up.html', kwargs)


@base_decorator
def article_view(request, article_id, *args, **kwargs):
    try:
        article_id = int(article_id)
        article = models.Article.objects.get(id=article_id)
    except Exception:
        raise Http404()
    finally:
        pass

    return render_to_response('article.html', {'article': article, **kwargs})
