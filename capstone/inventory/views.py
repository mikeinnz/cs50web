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
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

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

    if customer not in request.user.customers.all():
        # TODO: show message instead of JsonResponse
        return JsonResponse({"error": "Access denined."}, status=404)

    if request.method == "POST":
        save_customer(request, customer)
        return HttpResponseRedirect(reverse("list_customer"))

    else:
        return render(request, "inventory/customer_form.html", {
            'edit': True,
            'contact_form': CustomerContactForm(instance=customer),
            'billing_form': CustomerBillingForm(instance=customer),
            'shipping_form': CustomerShippingForm(instance=customer)
        })


@login_required
def warehouse(request):
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    warehouses = Warehouse.objects.filter(
        user=request.user).order_by('warehouse')
    return render(request, "inventory/warehouse.html", {
        'warehouses': warehouses
    })


@login_required
def create_warehouse(request):
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    if request.method == "POST":
        warehouse = Warehouse(user=request.user)
        warehouse_form = WarehouseForm(
            request.POST or None, instance=warehouse)
        if warehouse_form.is_valid:
            warehouse_form.save()
        return HttpResponseRedirect(reverse("warehouse"))

    else:
        return render(request, "inventory/warehouse_form.html", {
            "form": WarehouseForm()
        })


@login_required
def edit_warehouse(request, id):
    try:
        warehouse = Warehouse.objects.get(pk=id)
    except Warehouse.DoesNotExist:
        return JsonResponse({"error": "Warehouse not found."}, status=404)

    if warehouse not in request.user.warehouses.all():
        # TODO: show message instead of JsonResponse
        return JsonResponse({"error": "Access denined."}, status=404)

    if request.method == "POST":
        warehouse_form = WarehouseForm(
            request.POST or None, instance=warehouse)
        if warehouse_form.is_valid:
            warehouse_form.save()
        return HttpResponseRedirect(reverse("warehouse"))

    else:
        return render(request, "inventory/warehouse_form.html", {
            "edit": True,
            "form": WarehouseForm(instance=warehouse)
        })


@login_required
def product(request):
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    products = Product.objects.filter(user=request.user).order_by('name')
    return render(request, "inventory/product.html", {
        'products': products,
    })


@login_required
def create_product(request):
    return render(request, "inventory/product_form.html", {
        'form': ProductForm(request.user),
    })


@login_required
def edit_product(request):
    return HttpResponse("edit product")


@login_required
def create_category(request):
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    if request.method == "POST":
        category = ProductCategory(user=request.user)
        category_form = ProductCategoryForm(
            request.POST or None, instance=category)
        if category_form.is_valid:
            category_form.save()
        return HttpResponseRedirect(reverse("create_category"))

    else:
        return render(request, "inventory/category_form.html", {
            "form": ProductCategoryForm(),
            'categories': ProductCategory.objects.filter(user=request.user)
        })


@login_required
def edit_category(request, id):
    try:
        category = ProductCategory.objects.get(pk=id)
    except ProductCategory.DoesNotExist:
        return JsonResponse({"error": "Category not found."}, status=404)

    if category not in request.user.categories.all():
        # TODO: show message instead of JsonResponse
        return JsonResponse({"error": "Access denined."}, status=404)

    if request.method == "POST":
        category_form = ProductCategoryForm(
            request.POST or None, instance=category)
        if category_form.is_valid:
            category_form.save()
        return HttpResponseRedirect(reverse("create_category"))

    else:
        return render(request, "inventory/category_form.html", {
            "edit": True,
            "form": ProductCategoryForm(instance=category)
        })


@login_required
def order(request):
    return render(request, "inventory/sales_order.html", {

    })


@login_required
def create_order(request):
    return HttpResponse("create sales order")


@login_required
def edit_order(request):
    return HttpResponse("edit order")


@login_required
def create_sales_channel(request):
    return HttpResponse("create channel")
