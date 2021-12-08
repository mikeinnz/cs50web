from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import *
from .util import paginate_items, save_customer


@login_required
def index(request):
    """
    Dashboard
    """
    # Current month and last month in number
    today = datetime.now()
    current_month = today.month

    if current_month == 1:
        last_month = current_month - 12
    else:
        last_month = current_month - 1

    # Last quarter first date and last date
    if current_month < 4:
        first_date_last_quarter = date(today.year - 1, 10, 1)
        last_date_last_quarter = date(today.year - 1, 12, 31)
    elif current_month < 7:
        first_date_last_quarter = date(today.year, 1, 1)
        last_date_last_quarter = date(today.year, 3, 31)
    elif current_month < 10:
        first_date_last_quarter = date(today.year, 4, 1)
        last_date_last_quarter = - date(today.year, 6, 30)
    else:
        first_date_last_quarter = date(today.year, 7, 1)
        last_date_last_quarter = date(today.year, 9, 30)

    # Calculate last quarter's sales
    last_quarter_orders = SalesOrder.objects.filter(
        user=request.user, invoice_date__gte=first_date_last_quarter, invoice_date__lte=last_date_last_quarter)
    sales_last_quarter = 0
    for order in last_quarter_orders:
        items = SalesItem.objects.filter(order=order)
        for item in items:
            sales_last_quarter += item.sub_total()

    # Top sales (last 90 days)
    last_90_days_orders = SalesOrder.objects.filter(
        user=request.user, invoice_date__gte=today-timedelta(days=90)).order_by('-created_date')
    # Add order values to order list
    last_90_days_orders = add_order_values(last_90_days_orders)

    # Top 5 orders by value
    top_orders = sorted(last_90_days_orders,
                        key=lambda o: o.value, reverse=True)[:5]

    # Recent sales (top 5)
    recent_orders = SalesOrder.objects.filter(
        user=request.user).order_by('-created_date')[:5]
    # Add order values to order list
    recent_orders = add_order_values(recent_orders)

    # Top selling products and Top selling category (last 90 days)
    values_by_product = {}
    values_by_category = {}
    for order in last_90_days_orders:
        items = SalesItem.objects.filter(order=order)
        for item in items:
            product = item.product
            category = item.product.category.category
            if not product in values_by_product:
                values_by_product[product] = 0
            values_by_product[product] += item.sub_total()
            if not category in values_by_category:
                values_by_category[category] = 0
            values_by_category[category] += item.sub_total()

    sales_by_product = sorted(
        values_by_product.items(), key=lambda i: i[1], reverse=True)[:5]
    sales_by_category = sorted(
        values_by_category.items(), key=lambda i: i[1], reverse=True)[:5]

    return render(request, "inventory/index.html", {
        'sales_current_month': sales(request, current_month),
        'sales_last_month': sales(request, last_month),
        'sales_last_quarter': sales_last_quarter,
        'top_orders': top_orders,
        'recent_orders': recent_orders,
        'sales_by_category': sales_by_category,
        'sales_by_product': sales_by_product,
    })


def sales(request, month):
    orders = SalesOrder.objects.filter(
        user=request.user, invoice_date__month=month)

    sum = 0
    for order in orders:
        items = SalesItem.objects.filter(order=order)
        for item in items:
            sum += item.sub_total()
    return sum


def add_order_values(orders):
    for order in orders:
        order.value = 0
        for item in SalesItem.objects.filter(order=order):
            order.value += item.sub_total()
    return orders


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
    # try:
    #     customer = Customer.objects.get(pk=id, user=request.user)
    # except Customer.DoesNotExist:
    #     return JsonResponse({"error": "Customer not found."}, status=404)
    # Use the above option or simply use get_object_or_404
    customer = get_object_or_404(Customer, pk=id, user=request.user)

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
        user=request.user).order_by('warehouse', '-product')
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
            "form": WarehouseForm(),
            "warehouses": Warehouse.objects.filter(user=request.user)
        })


@login_required
def edit_warehouse(request, id):
    """
    Edit a warehouse (name only)
    """
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    warehouse = get_object_or_404(Warehouse, pk=id, user=request.user)

    if request.method == "POST":
        warehouse_form = WarehouseForm(
            request.POST or None, instance=warehouse)
        if warehouse_form.is_valid:
            warehouse_form.save()
        return HttpResponseRedirect(reverse("warehouse"))

    else:
        return render(request, "inventory/warehouse_form.html", {
            "edit": True,
            "form": WarehouseForm(instance=warehouse),
            "warehouses": Warehouse.objects.filter(user=request.user)
        })


@login_required
def view_warehouse(request, id):
    """
    View a specified warehouse's inventory
    """
    warehouse = get_object_or_404(Warehouse, pk=id, user=request.user)

    shelves = Shelf.objects.filter(
        user=request.user, warehouse=warehouse).order_by('-product')
    return render(request, "inventory/warehouse.html", {
        'warehouses': warehouse,
        'shelves': shelves,
        'view': True
    })


@login_required
def warehouse_api(request, id):
    """
    Return a warehouse's inventory data as a json response
    """
    try:
        warehouse = Warehouse.objects.get(pk=id, user=request.user)
    except Warehouse.DoesNotExist:
        return JsonResponse({"error": "Warehouse not found."}, status=404)

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
    product = get_object_or_404(Product, pk=id, user=request.user)

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
    category = get_object_or_404(ProductCategory, pk=id, user=request.user)

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
    View Sales Orders in a table with search form
    """

    # Set default orders excluding closed ones
    sales_orders = SalesOrder.objects.filter(
        user=request.user).exclude(status=SalesOrder.CLOSED).order_by('-id')
    date_form = SearchDateForm()
    status_form = SearchStatusForm()

    if request.method == "POST":
        # Save search input into session
        request.session['post_data'] = request.POST

    # Retrieve user input from session
    if 'post_data' in request.session:
        data = request.session['post_data']

        if 'date_type' in data:
            date_form = SearchDateForm(data)
            if date_form.is_valid():
                from_date = date_form.cleaned_data['from_date']
                to_date = date_form.cleaned_data['to_date']
                if from_date is not None and to_date is not None:
                    if data['date_type'] == SearchDateForm.CREATED_DATE:
                        sales_orders = SalesOrder.objects.filter(
                            user=request.user, created_date__gte=from_date, created_date__lte=to_date).order_by('-created_date')
                    elif data['date_type'] == SearchDateForm.INVOICE_DATE:
                        sales_orders = SalesOrder.objects.filter(
                            user=request.user, invoice_date__gte=from_date, invoice_date__lte=to_date).order_by('-invoice_date')

        elif 'status' in data and data['status'] != '':
            status_form = SearchStatusForm(data)
            if status_form.is_valid():
                status = status_form.cleaned_data['status']
                sales_orders = SalesOrder.objects.filter(
                    user=request.user, status=status).order_by('-id')

        elif 'search' in data:
            if data['search'] == 'show_all':
                sales_orders = SalesOrder.objects.filter(
                    user=request.user).order_by('-id')
            elif data['search'] == 'reset':
                # Set default orders excluding closed ones
                sales_orders = SalesOrder.objects.filter(
                    user=request.user).exclude(status=SalesOrder.CLOSED).order_by('-id')

    # Add order values to order list
    for order in sales_orders:
        order.value = 0
        for item in SalesItem.objects.filter(order=order):
            order.value = order.value + item.sub_total()

    return render(request, "inventory/sales_order.html", {
        "date_form": date_form,
        "status_form": status_form,
        "page_obj": paginate_items(request, sales_orders)
    })


@login_required
def order_api(request):
    all_orders = SalesOrder.objects.filter(user=request.user).order_by('-id')
    return JsonResponse([order.serialize() for order in all_orders], safe=False)


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

    success = False
    if request.method == "POST":
        if formset.is_valid() and order_form.is_valid():
            # Save items and deduct from shelves
            success = save_sales_order(request, order, order_form, formset)

    return render(request, "inventory/sales_order_form.html", {
        'success': success,
        'order_form': order_form,
        'item_formset': formset,
    })


@login_required
def edit_order(request, id):
    """
    Edit a sales order
    """

    order = get_object_or_404(SalesOrder, pk=id, user=request.user)

    # Remember the original warehouse
    warehouse = order.warehouse

    data = request.POST or None
    order_form = SalesOrderForm(request.user, data, instance=order)

    SalesItemFormSet = formset_factory(SalesItemForm, extra=1)

    # by default, sales_items_list returns 'product_id' as a key (since product is a Foreign Key field defined in the model),
    # but in order to pass as an initial data to pre-populate the selected option in the drop-down box for products, the key needs to be 'product'
    sales_items = SalesItem.objects.filter(order=order)
    sales_items_list = list(sales_items.values())
    # change key from product_id to product
    for i in sales_items_list:
        i['product'] = i.pop('product_id')

    # pre-populate item details
    formset = SalesItemFormSet(data, initial=sales_items_list)

    success = False
    if request.method == 'POST':
        if formset.is_valid() and order_form.is_valid():

            # Remove existing items and return to shelves
            for item in sales_items:
                shelf = Shelf.objects.get(
                    user=request.user, warehouse=warehouse, product=item.product)
                shelf.quantity = shelf.quantity + item.quantity
                shelf.save()
            sales_items.delete()

            # Save items and deduct from shelves
            success = save_sales_order(request, order, order_form, formset)

    # Pre-populate only products available in the selected warehouse
    shelves_have_products = Shelf.objects.filter(
        user=request.user, warehouse=order.warehouse)
    product_ids = [s.product.id for s in shelves_have_products]
    for form in formset:
        form.fields['product'].queryset = Product.objects.filter(
            pk__in=product_ids).order_by('name')

    return render(request, "inventory/sales_order_form.html", {
        'edit': True,
        'success': success,
        'order_form': order_form,
        'item_formset': formset,
    })


def save_sales_order(request, order, order_form, formset):
    # Set invoice_number incrementally (same as id)
    if order.invoice_number is None:
        order.invoice_number = SalesOrder.objects.all().last().id + 1

    saved = False

    for f in formset:
        item = f.save(commit=False)
        item.order = order

        # Save only items where product was selected
        if hasattr(item, 'product'):
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

    return saved


@login_required
def create_sales_channel(request):
    """
    Create a new sales channel
    """
    if not request.user.is_authenticated:
        return JsonResponse(status=404)

    if request.method == "POST":
        channel = SalesChannel(user=request.user)
        channel_form = SalesChannelForm(
            request.POST or None, instance=channel)
        if channel_form.is_valid:
            channel_form.save()
        return HttpResponseRedirect(reverse("order"))

    else:
        return render(request, "inventory/channel_form.html", {
            "form": SalesChannelForm(),
            'channels': SalesChannel.objects.filter(user=request.user)
        })


@login_required
def edit_sales_channel(request, id):
    """
    Edit a sales channel (name only)
    """
    channel = get_object_or_404(SalesChannel, pk=id, user=request.user)

    if request.method == "POST":
        channel_form = SalesChannelForm(
            request.POST or None, instance=channel)
        if channel_form.is_valid:
            channel_form.save()
        return HttpResponseRedirect(reverse("create_sales_channel"))

    else:
        return render(request, "inventory/channel_form.html", {
            "edit": True,
            "form": SalesChannelForm(instance=channel)
        })
