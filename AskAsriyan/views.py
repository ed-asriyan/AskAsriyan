from django.http.response import HttpResponse
from django.shortcuts import render_to_response
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
        
        return func(request, kwargs, tags=tags)

    return decorator


@base_decorator
def sign_in_view(request, *args, **kwargs):
    return render_to_response('sign_in.html', kwargs)
