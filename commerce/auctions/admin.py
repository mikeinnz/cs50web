from django.contrib import admin
from django.db.models.fields import BinaryField, BooleanField
from .models import Category, Listing, Comment, Bid, User,  Watchlist, Winner


# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Winner)
