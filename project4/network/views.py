import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import Follow, Like, Post, User
from .util import paginate_posts


def index(request):
    if request.method == "POST":
        content = request.POST["content"]
        if content != "":
            p = Post(author=request.user, content=content)
            p.save()

    posts = Post.objects.all().order_by('-timestamp')

    return render(request, "network/index.html", {
        "heading": "All Posts",
        'page_obj': paginate_posts(request, posts),
    })


def profile(request, id):
    u = User.objects.get(pk=id)
    posts = Post.objects.filter(author=u).order_by('-timestamp')

    is_following = False
    if request.user.is_authenticated:
        if u in [f.user for f in request.user.following.all()]:
            is_following = True

    return render(request, "network/profile.html", {
        "profile": u,
        "page_obj": paginate_posts(request, posts),
        "num_followers": u.followers.all().count(),
        "num_following": u.following.all().count(),
        "is_following": is_following,
    })


@csrf_exempt
def edit(request, id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)

        if data.get("content") is not None:
            # TODO why Model does not check max length
            post.content = data["content"]
        post.save()
        return JsonResponse({"message": "Edit successfully."}, status=201)

    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


# TODO: remove @csrf_exempt
@csrf_exempt
def follow(request, id):

    try:
        u = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

    if request.method == "GET":
        is_following = False
        if request.user.is_authenticated:
            if u in [f.user for f in request.user.following.all()]:
                is_following = True

        return JsonResponse({"is_following": is_following,
                             "num_followers": u.followers.all().count(),
                             })

    elif request.method == "PUT":
        data = json.loads(request.body)

        # Follow
        if data.get("follow"):
            # Only update database when there is no similar record and ensure user is not following themselves
            if not Follow.objects.filter(user=u, follower=request.user).exists() and u != request.user:
                follow = Follow(user=u, follower=request.user)
                follow.save()

        # Unfollow
        else:
            # Remove record from database
            follow = Follow.objects.filter(user=u, follower=request.user)
            follow.delete()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@login_required
def following(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(
        author__in=[f.user for f in user.following.all()]).order_by('-timestamp')

    return render(request, "network/index.html", {
        "heading": "Following",
        "page_obj": paginate_posts(request, posts),
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
