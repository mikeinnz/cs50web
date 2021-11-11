from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    starting_bid = models.FloatField()
    active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(blank=True, max_length=200)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.title} (id: {self.id}) created by {self.owner}"


class Winner(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="winner")
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="won")

    def __str__(self):
        return f"{self.winner}"


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=526)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment} by {self.user} at {self.timestamp}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watching_users")

    def __str__(self):
        return f"{self.user} watching {self.listing}"


class Bid(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    bidding_price = models.IntegerField()
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidding")
    timestamp = models.DateTimeField(auto_now_add=True)
