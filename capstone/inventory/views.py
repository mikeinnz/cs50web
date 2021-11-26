from django.contrib.auth import logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "inventory/index.html")


def create_customer(request):

    if request.method == "POST":
        customer = Customer()

        contact = CustomerContactForm(request.POST or None, instance=customer)
        billing = CustomerBillingForm(request.POST or None, instance=customer)
        shipping = CustomerShippingForm(
            request.POST or None, instance=customer)
        if contact.is_valid and billing.is_valid and shipping.is_valid:
            contact.save()
            billing.save()
            shipping.save()
            return HttpResponse("OKAY")

    else:
        return render(request, "inventory/customer_create.html", {
            'contact_form': CustomerContactForm(),
            'billing_form': CustomerBillingForm(),
            'shipping_form': CustomerShippingForm()
        })


def login_view(request):

    if request.method == "POST":
        return HttpResponse("POST")
    else:
        return render(request, "inventory/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
