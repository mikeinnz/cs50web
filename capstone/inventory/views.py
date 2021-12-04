from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.forms import formset_factory, modelform_factory
from django.forms.models import modelform_factory, modelformset_factory
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .util import paginate_items, save_customer


def index(request):
    return render(request, "inventory/index.html")


@login_required
def create_customer(request):
    """
    Create a new customer
    """
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
    """
    View a list of customers
    """
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    customers = Customer.objects.filter(
        user=request.user).order_by('first_name')

    return render(request, "inventory/customer_list.html", {
        "page_obj": paginate_items(request, customers)
    })


@login_required
def edit_customer(request, id):
    """
    Edit a customer
    """
    try:
        customer = Customer.objects.get(pk=id, user=request.user)
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found."}, status=404)
        # TODO: show message instead of JsonResponse - try get_object_or_404

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
    """
    View all warehouses' inventory
    """
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    warehouses = Warehouse.objects.filter(
        user=request.user).order_by('warehouse')

    shelves = Shelf.objects.filter(
        user=request.user).order_by('warehouse')
    return render(request, "inventory/warehouse.html", {
        'warehouses': warehouses,
        'shelves': shelves
    })


@login_required
def create_warehouse(request):
    """
    Create a new warehouse (name only)
    """
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
    """
    Edit a warehouse (name only)
    """
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    try:
        warehouse = Warehouse.objects.get(pk=id, user=request.user)
    except Warehouse.DoesNotExist:
        return JsonResponse({"error": "Warehouse not found."}, status=404)

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
def view_warehouse(request, id):
    """
    View a specified warehouse's inventory
    """
    try:
        warehouse = Warehouse.objects.get(pk=id, user=request.user)
    except Warehouse.DoesNotExist:
        return JsonResponse({"error": "Warehouse not found."}, status=404)
        # TODO: show message instead of JsonResponse

    shelves = Shelf.objects.filter(user=request.user, warehouse=warehouse)
    return render(request, "inventory/warehouse.html", {
        'warehouses': warehouse,
        'shelves': shelves,
        'view': True
    })


@login_required
def warehouse_api(request, id):
    try:
        warehouse = Warehouse.objects.get(pk=id, user=request.user)
    except Warehouse.DoesNotExist:
        return JsonResponse({"error": "Warehouse not found."}, status=404)
        # TODO: show message instead of JsonResponse

    shelves = Shelf.objects.filter(
        user=request.user, warehouse=warehouse)
    # return JsonResponse({"shelves": list(shelves.values())})
    return JsonResponse([shelf.serialize() for shelf in shelves], safe=False)


@login_required
def product(request):
    """
    View a list of products
    """
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    products = Product.objects.filter(user=request.user).order_by('name')
    return render(request, "inventory/product.html", {
        'page_obj': paginate_items(request, products),
    })


@login_required
def create_product(request):
    """
    Create a new product
    """
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    if request.method == "POST":
        product = Product(user=request.user)
        product_form = ProductForm(
            request.user, request.POST or None, instance=product)
        if product_form.is_valid:
            product_form.save()
        return HttpResponseRedirect(reverse("product"))

    else:
        return render(request, "inventory/product_form.html", {
            'form': ProductForm(request.user),
        })


@login_required
def edit_product(request, id):
    """
    Edit a product
    """
    try:
        product = Product.objects.get(pk=id, user=request.user)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)
        # TODO: show message instead of JsonResponse

    if request.method == "POST":
        product_form = ProductForm(request.user,
                                   request.POST or None, instance=product)
        if product_form.is_valid:
            product_form.save()
        return HttpResponseRedirect(reverse("product"))

    else:
        return render(request, "inventory/product_form.html", {
            "edit": True,
            "form": ProductForm(request.user, instance=product)
        })


@login_required
def create_category(request):
    """
    Create a new category
    """
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
    """
    Edit a category (name only)
    """
    try:
        category = ProductCategory.objects.get(pk=id, user=request.user)
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
    """
    View Sales Orders
    """
    return render(request, "inventory/sales_order.html", {
        "orders": SalesOrder.objects.filter(user=request.user).order_by('-id')
    })


@login_required
def create_order(request):
    """
    Create a new sales order and update inventory
    """

    data = request.POST or None
    order = SalesOrder(user=request.user)
    order_form = SalesOrderForm(request.user, data, instance=order)

    SalesItemFormSet = formset_factory(SalesItemForm)
    formset = SalesItemFormSet(data)

    # Filter products belonging to the current user
    for form in formset:
        form.fields['product'].queryset = Product.objects.filter(
            user=request.user).order_by('name')

    if request.method == "POST":
        if formset.is_valid() and order_form.is_valid():
            order.invoice_number = '123'  # TODO auto generate
            saved = False

            for f in formset:
                item = f.save(commit=False)
                item.order = order

                # Save only items where product was selected
                if hasattr(item, 'product'):
                    print("ITEM:")
                    print(item)
                    shelf = Shelf.objects.get(
                        user=request.user, warehouse=order.warehouse, product=item.product)

                    # has enough inventory and quantity, price & discount must not be negative
                    if shelf.quantity >= item.quantity and item.quantity > 0 and item.price >= 0 and item.discount >= 0:
                        if (not saved):
                            # Save order before its items
                            order_form.save()
                            saved = True
                        item.save()
                        # Update inventory
                        shelf.quantity = shelf.quantity - item.quantity
                        shelf.save()

            if saved:
                return HttpResponseRedirect(reverse("order"))

    return render(request, "inventory/sales_order_form.html", {
        'order_form': order_form,
        'item_formset': formset,
    })


@login_required
def edit_order(request, id):
    """
    Edit a sales order
    """

    try:
        order = SalesOrder.objects.get(pk=id, user=request.user)
    except SalesOrder.DoesNotExist:
        return JsonResponse({"error": "Sales Order not found."}, status=404)

    order_form = SalesOrderForm(request.user, instance=order)

    SalesItemFormSet = formset_factory(SalesItemForm, extra=0)

    # by default, sales_items_list returns 'product_id' as a key (since product is a Foreign Key field defined in the model),
    # but in order to pass as an initial data to pre-populate the selected option in the drop-down box for products, the key needs to be 'product'
    sales_items = SalesItem.objects.filter(order=order)
    sales_items_list = list(sales_items.values())
    # change key from product_id to product
    for i in sales_items_list:
        i['product'] = i.pop('product_id')

    # pre-populate item details
    formset = SalesItemFormSet(initial=sales_items_list)

    # Pre-populate only products available in the selected warehouse
    shelves_have_products = Shelf.objects.filter(
        user=request.user, warehouse=order.warehouse)
    product_ids = [s.product.id for s in shelves_have_products]
    for form in formset:
        form.fields['product'].queryset = Product.objects.filter(
            pk__in=product_ids).order_by('name')

    print(formset)

    # TODO prepopulate order value, and formate quantity & price to 2 decimal places

    return render(request, "inventory/sales_order_form.html", {
        'edit': True,
        'order_form': order_form,
        'item_formset': formset,
    })


@login_required
def create_sales_channel(request):
    return HttpResponse("create channel")
