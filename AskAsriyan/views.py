from django.http.response import HttpResponse
from django.shortcuts import render_to_response


def sign_in_page(request):
    return render_to_response('sign_in.html')