from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("hello, world!")


def login(request):

    if request.method == "POST":
        return HttpResponse("POST")
    else:
        return render(request, "inventory/login.html")
