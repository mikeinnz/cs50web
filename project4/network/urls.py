
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following/<int:id>", views.following, name="following"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("edit/<int:postid>", views.edit, name="edit"),
    path("post/<int:postid>", views.post, name="post"),
]
