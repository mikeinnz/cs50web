from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .util import list_with_current_price
from .models import Bid, Category, Comment, Listing, User, Watchlist, Winner


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description",
                  "starting_bid", "image_url", "category"]


def index(request):
    # Sort by latest created time
    listings = Listing.objects.filter(active=True).order_by('-created_time')

    return render(request, "auctions/index.html", {
        "listings": list_with_current_price(listings),
    })


# Add comment
@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        if comment != "":
            listing = Listing.objects.get(pk=listing_id)
            c = Comment(listing=listing,
                        user=request.user, comment=comment)
            c.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Place a bid
@login_required
def bidding(request, listing_id):

    if request.method == "POST":
        price = int(request.POST["bid"])
        bids = Bid.objects.filter(listing=listing_id)

        listing = Listing.objects.get(pk=listing_id)

        if bids:
            current_price = bids.aggregate(
                Max('bidding_price')).get('bidding_price__max')
        else:
            current_price = listing.starting_bid

        if price <= current_price:
            return render(request, "auctions/listing.html", {
                "message": "Bid must be higher than the current price"
            })

        b = Bid(listing=listing, bidding_price=price, bidder=request.user)
        b.save()

        # Re-render the listing details
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Close a listing
@login_required
def close(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)

    # Query the bids database
    bids = Bid.objects.filter(listing=listing_id)
    highest_bid = bids.order_by('-bidding_price').first()

    # Make the highest bidder the winner
    if highest_bid:
        # Save to Winner database
        w = Winner(listing=listing, winner=highest_bid.bidder)
        w.save()

    # Make the listing inactive
    listing.active = False
    listing.save()

    # Re-render the listing details
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Create a new listing
@ login_required
def create(request):

    if request.method == "POST":
        # Save the submited data to a form
        form = ListingForm(request.POST)

        # Check if form data is valid
        if form.is_valid():
            form = form.cleaned_data

            listing = Listing(title=form["title"], description=form["description"], starting_bid=form["starting_bid"],
                              image_url=form["image_url"], category=form["category"], owner=request.user)
            listing.save()

            # Redirect to the listing details page
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": ListingForm()
    })


# Render listing details
def listing(request, listing_id):

    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {
            "message": "Listing does not exist."
        })

    winner = None
    if Winner.objects.filter(listing=listing_id):
        winner = Winner.objects.get(listing=listing_id)

    in_watchlist = False
    if request.user.is_authenticated:
        wlitems = Watchlist.objects.filter(user=request.user)
        if listing in [w.listing for w in wlitems]:
            in_watchlist = True

    bids = Bid.objects.filter(listing=listing_id)
    bid_count = 0
    highest_bidder = None
    if bids:
        b = bids.order_by('-bidding_price').first()
        current_price = b.bidding_price
        bid_count = bids.count()
        highest_bidder = b.bidder
    else:
        current_price = listing.starting_bid

    comments = Comment.objects.filter(listing=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "winner": winner,
        "in_watchlist": in_watchlist,
        "bid_count": bid_count,
        "highest_bidder": highest_bidder,
        "current_price": current_price,
    })


# Render all listing categories
def categories(request):
    categories = Category.objects.all()

    clist = []
    for i in categories:
        i.listing_count = Listing.objects.filter(
            category=i, active=True).count()
        clist.append(i)

    return render(request, "auctions/categories.html", {
        "categories": clist
    })


# Render all listings in a selected category
def category(request, id):
    category = Category.objects.get(pk=id)

    # Only get active listings
    listings = category.listings.filter(active=True)

    return render(request, "auctions/index.html", {
        "listings": list_with_current_price(listings),
        "category": category,
    })


# Process a watchlist action
@ login_required
def update_watchlist(request, listing_id):

    wl = Watchlist.objects.filter(user=request.user, listing=listing_id)
    if wl:
        wl.delete()
    else:
        wl = Watchlist(user=request.user,
                       listing=Listing.objects.get(pk=listing_id))
        wl.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Render a Watchlist page
@ login_required
def watchlist(request):
    wlitems = Watchlist.objects.filter(user=request.user)

    listings = [i.listing for i in wlitems]

    return render(request, "auctions/index.html", {
        "listings": list_with_current_price(listings),
        "watchlist": True,
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

            next_url = request.POST.get('next')
            if next_url:
                # Redirect to the page prior to login
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
