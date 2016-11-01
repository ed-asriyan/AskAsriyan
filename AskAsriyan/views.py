from django.http.response import HttpResponse
from django.shortcuts import render_to_response


def BasePage(request, content=""):
    return render_to_response('base.html', {'content': content})
