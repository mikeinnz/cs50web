from django.contrib.auth import logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    return HttpResponse("hello, world!")


def login_view(request):

    if request.method == "POST":
        return HttpResponse("POST")
    else:
        return render(request, "inventory/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
