from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import ModelForm

from datetime import date


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="customers")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    phone = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=256)
    billing_street = models.CharField(blank=True, max_length=128)
    billing_suburb = models.CharField(blank=True, max_length=64)
    billing_city = models.CharField(blank=True, max_length=64)
    billing_postcode = models.CharField(blank=True, max_length=8)
    billing_country = models.CharField(blank=True, max_length=64)
    shipping_street = models.CharField(blank=True, max_length=128)
    shipping_suburb = models.CharField(blank=True, max_length=64)
    shipping_city = models.CharField(blank=True, max_length=64)
    shipping_postcode = models.CharField(blank=True, max_length=6)
    shipping_country = models.CharField(blank=True, max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{ self.first_name } { self.last_name }"


class CustomerContactForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name',
                  'company', 'email', 'phone', 'note']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'})
        }


class CustomerBillingForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['billing_street', 'billing_suburb',
                  'billing_city', 'billing_postcode', 'billing_country']
        widgets = {
            'billing_street': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_suburb': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_city': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_country': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomerShippingForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['shipping_street', 'shipping_suburb',
                  'shipping_city', 'shipping_postcode', 'shipping_country']
        widgets = {
            'shipping_street': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_suburb': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_country': forms.TextInput(attrs={'class': 'form-control'}),
        }


class Warehouse(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="warehouses")
    warehouse = models.CharField(max_length=64)

    def __str__(self):
        return f"{ self.warehouse }"


class WarehouseForm(ModelForm):
    class Meta:
        model = Warehouse
        fields = ['warehouse']
        widgets = {
            'warehouse': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
        }


class ProductCategory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories")
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{ self.category }"


class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['category']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
        }


class SalesChannel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sales_channels")
    channel = models.CharField(max_length=64)

    def __str__(self):
        return f"{ self.channel }"


class SalesChannelForm(ModelForm):
    class Meta:
        model = SalesChannel
        fields = ['channel']
        widgets = {
            'channel': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
        }


class Product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    sku = models.CharField(blank=True, max_length=20)
    barcode = models.CharField(blank=True, max_length=32)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, related_name="products")
    batch = models.CharField(max_length=20)
    expiry_date = models.DateField(null=True, blank=True)
    unit_cost = models.DecimalField(
        max_digits=19, decimal_places=10, default=0)
    retail_price = models.DecimalField(
        max_digits=19, decimal_places=10, default=1)

    def __str__(self):
        return f"{ self.name }"


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '1e1', 'min': '0'}),
            'retail_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '1e1', 'min': '0'}),
        }

    # dynamically filter Category belonging to the current user
    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = ProductCategory.objects.filter(
            user=user).order_by('category')


class SalesOrder(models.Model):
    DRAFT = 'DRAFT'
    CREATED = 'CREATED'
    INVOICED = 'INVOICED'
    DISPATCHED = 'DISPATCHED'
    PAID = 'PAID'
    CLOSED = 'CLOSED'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (CREATED, 'Created'),
        (INVOICED, 'Invoiced'),
        (DISPATCHED, 'Dispatched'),
        (PAID, 'Paid'),
        (CLOSED, 'Closed')
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sales_orders")
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders")
    created_date = models.DateField(default=date.today)
    invoice_date = models.DateField(default=date.today)
    invoice_number = models.IntegerField()
    channel = models.ForeignKey(
        SalesChannel, blank=True, null=True, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    reference = models.CharField(max_length=32, blank=True)
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default=CREATED)
    tracking = models.CharField(max_length=256, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order No. { self.id }"

    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'created_date': self.created_date,
    #         'invoice_date': self.invoice_date,
    #         'first_name': self.customer.first_name,
    #         'last_name': self.customer.last_name,
    #         'status': self.status,
    #         'channel': self.channel.channel,  # TODO: when channel is None type, fix erros
    #         'warehouse': self.warehouse.warehouse,
    #         'value': sum(i.sub_total() for i in self.items.all())
    #     }


class SalesOrderForm(ModelForm):
    class Meta:
        model = SalesOrder
        exclude = ['user', 'invoice_number', 'timestamp']
        widgets = {
            'created_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'tracking': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'channel': forms.Select(attrs={'class': 'form-select'}),
            'warehouse': forms.Select(attrs={'class': 'form-select col-auto'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(SalesOrderForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(
            user=user).order_by('first_name')
        self.fields['channel'].queryset = SalesChannel.objects.filter(
            user=user).order_by('channel')
        self.fields['warehouse'].queryset = Warehouse.objects.filter(
            user=user).order_by('warehouse')


class SearchDateForm(forms.Form):
    CREATED_DATE = 'CREATED_DATE'
    INVOICE_DATE = 'INVOICE_DATE'

    CHOICES = [
        ('', '---------'),
        (CREATED_DATE, 'Created date'),
        (INVOICE_DATE, 'Invoice date'),
    ]
    date_type = forms.ChoiceField(label='Search by date', choices=CHOICES, widget=forms.Select(
        attrs={'class': 'form-select'}), required=False)
    from_date = forms.DateField(
        label='From', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    to_date = forms.DateField(
        label='To', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)


class SearchStatusForm(forms.Form):
    # Add empty selection to STATUS_CHOICES
    CHOICES = [('', '---------')] + SalesOrder.STATUS_CHOICES

    # Submit form on dropdown selection
    status = forms.ChoiceField(
        label='Search by status', choices=CHOICES, widget=forms.Select(
            attrs={'class': 'form-select', 'onChange': 'form.submit()'}), required=False)


class SalesItem(models.Model):
    order = models.ForeignKey(
        SalesOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(
        max_digits=19, decimal_places=10, default=1)
    price = models.DecimalField(
        max_digits=19, decimal_places=10, default=1)
    discount = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def sub_total(self):
        return self.quantity * (1 - self.discount) * self.price

    def __str__(self):
        return f"{ self.order}: { self.quantity } x { self.product }"


class SalesItemForm(ModelForm):
    class Meta:
        model = SalesItem
        exclude = ['order']
        # set up each field with the same class 'value' in order to calculate order value in javascript
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select value'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control value', 'step': '1e-1', 'min': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control value', 'step': '1e-2', 'min': '0'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control value', 'step': '1e-1', 'min': '0'})
        }
        labels = {
            'product': 'Product [Available]',
        }

    # def __init__(self, user, *args, **kwargs):
    #     super(SalesItemForm, self).__init__(*args, **kwargs)
    #     self.fields['product'].queryset = Product.objects.filter(user=user)


class Shelf(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shelves")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=19, decimal_places=10, default=0)

    def __str__(self):
        return f"At { self.warehouse }, { self.user } has { self.quantity } x { self.product }"

    def serialize(self):
        return {
            'user': self.user.username,
            'warehouse': self.warehouse.warehouse,
            'product_id': self.product.id,
            'product': self.product.name,
            'quantity': self.quantity,
        }
