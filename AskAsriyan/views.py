from django.http.response import HttpResponse
from django.shortcuts import render_to_response
import random

def base_decorator(func):
    def decorator(request, *args, **kwargs):
        tags = [''.join([chr(random.randint(ord('A'), ord('z'))) for j in range(0, random.randint(5, 10))]) for i in
                range(random.randint(15, 35))]
        print(tags)
        return func(request, kwargs, tags=tags)

    return decorator
