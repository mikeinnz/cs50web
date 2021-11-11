from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>",
         views.update_watchlist, name="update_watchlist"),
    path("category/<int:id>", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("bidding/<int:listing_id>", views.bidding, name="bidding"),
    path("close/<int:listing_id>", views.close, name="close"),
]
