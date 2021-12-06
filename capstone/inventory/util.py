from django.core.paginator import Paginator
from .models import CustomerContactForm, CustomerBillingForm, CustomerShippingForm


# Number of items per page
ITEMS_PER_PAGE = 8


def paginate_items(request, items):
    """
    Paginating items
    """
    paginator = Paginator(items, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def save_customer(request, customer):
    """
    Save customer to database
    """
    data = request.POST or None
    contact = CustomerContactForm(data, instance=customer)
    billing = CustomerBillingForm(data, instance=customer)
    shipping = CustomerShippingForm(
        data, instance=customer)
    if contact.is_valid and billing.is_valid and shipping.is_valid:
        contact.save()
        billing.save()
        shipping.save()
