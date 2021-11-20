import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse


from .models import Follow, Like, Post, User, POST_MAX_LENGTH
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


def post(request, postid):

    # Query for requested post
    try:
        post = Post.objects.get(pk=postid)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post details
    if request.method == "GET":
        return JsonResponse({"id": post.id,
                            "num_likes": post.liked_users.all().count(),
                             "liked": request.user in [like.user for like in post.liked_users.all()],
                             "logged_in": request.user.is_authenticated
                             })

    # Save like to database
    elif request.method == "PUT":

        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        else:
            data = json.loads(request.body)
            if data.get("like") is not None:
                if not Like.objects.filter(post=post, user=request.user).exists():
                    like = Like(post=post, user=request.user)
                    like.save()
                else:
                    like = Like.objects.filter(post=post, user=request.user)
                    like.delete()

        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def profile(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    posts = Post.objects.filter(author=user).order_by('-timestamp')

    return render(request, "network/profile.html", {
        "profile": user,
        "page_obj": paginate_posts(request, posts),
        "num_followers": user.followers.all().count(),
        "num_following": user.following.all().count(),
    })


@login_required
def edit(request, postid):

    # Query for requested post
    try:
        post = Post.objects.get(pk=postid)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)

        if data.get("content") is not None:
            post.content = data["content"]

        # Check max length
        if len(post.content) > POST_MAX_LENGTH:
            return JsonResponse({"error": "Must be less than 280 characters."}, status=404)
        post.save()
        return JsonResponse({"message": "Edit successfully."}, status=201)

    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


@login_required
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
            # Only update database when there is no existing record and ensure user is not following themselves
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
