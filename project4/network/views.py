from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Like, Post, User
from .util import posts_list_with_num_likes


def index(request):
    if request.method == "POST":
        content = request.POST["content"]
        if content != "":
            p = Post(author=request.user, content=content)
            p.save()

    posts = Post.objects.all().order_by('-timestamp')

    return render(request, "network/index.html", {
        "heading": "All Posts",
        "posts": posts_list_with_num_likes(posts),
    })


def profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(author=user).order_by('-timestamp')
    num_followers = user.followers.all().count()
    num_following = user.following.all().count()

    return render(request, "network/profile.html", {
        "username": user.username,
        "posts": posts_list_with_num_likes(posts),
        "num_followers": num_followers,
        "num_following": num_following,
    })


def following(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(
        author__in=[f.user for f in user.following.all()]).order_by('-timestamp')

    return render(request, "network/index.html", {
        "heading": "Following",
        "posts": posts_list_with_num_likes(posts),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
