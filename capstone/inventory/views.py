from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .util import paginate_customers, save_customer


def index(request):
    return render(request, "inventory/index.html")


@login_required
def create_customer(request):

    if request.method == "POST":
        customer = Customer()
        customer.user = request.user
        save_customer(request, customer)
        return HttpResponseRedirect(reverse("list_customer"))

    else:
        return render(request, "inventory/customer_form.html", {
            'contact_form': CustomerContactForm(),
            'billing_form': CustomerBillingForm(),
            'shipping_form': CustomerShippingForm()
        })


@login_required
def list_customer(request):
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    customers = Customer.objects.filter(
        user=request.user).order_by('first_name')

    return render(request, "inventory/customer_list.html", {
        "page_obj": paginate_customers(request, customers)
    })


@login_required
def edit_customer(request, id):

    try:
        customer = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found."}, status=404)

    if request.method == "POST":
        save_customer(request, customer)
        return HttpResponseRedirect(reverse("list_customer"))

    else:
        return render(request, "inventory/customer_form.html", {
            'title': "Edit Customer",
            'contact_form': CustomerContactForm(instance=customer),
            'billing_form': CustomerBillingForm(instance=customer),
            'shipping_form': CustomerShippingForm(instance=customer)
        })


@login_required
def warehouse(request):
    return render(request, "inventory/warehouse.html", {

    })
