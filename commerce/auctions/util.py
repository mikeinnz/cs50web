from .models import Bid
from django.db.models import Max


def list_with_current_price(listings):
    """
    Add an additional current_price field to the list of listings.
    The current_price is extracted from the bidding history
    """
    list = []
    for listing in listings:
        # Find the current price for each listing
        current_price = Bid.objects.filter(listing=listing).aggregate(
            Max('bidding_price')).get('bidding_price__max')

        if not current_price:
            current_price = listing.starting_bid

        # Add current_price as a new field to the list
        listing.current_price = current_price
        list.append(listing)
    return list
