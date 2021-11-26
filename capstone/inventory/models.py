from django import forms
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.forms import ModelForm, widgets

from datetime import date


STATUS_CHOICES = [
    ('DRAFT', 'Draft'),
    ('CREATED', 'Created'),
    ('INVOICED', 'Invoiced'),
    ('DISPATCHED', 'Dispatched'),
    ('PAID', 'Paid')
]


class Customer(models.Model):
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

    def __str__(self):
        return f"{ self.first_name } { self.last_name }"


class CustomerContactForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name',
                  'company', 'email', 'phone', 'note']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
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


# class Warehouse(models.Model):
#     branch = models.CharField(max_length=64)

#     def __str__(self):
#         return f"{ self.branch }"


# class ProductCategory(models.Model):
#     category = models.CharField(max_length=64)

#     def __str__(self):
#         return f"{ self.category }"


# class SalesChannel(models.Model):
#     channel = models.CharField(max_length=64)

#     def __str__(self):
#         return f"{ self.channel }"


# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     code = models.CharField(blank=True, max_length=20)
#     barcode = models.CharField(blank=True, max_length=32)
#     category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
#     batch = models.CharField(max_length=20)
#     expiry_date = models.DateField(blank=True)
#     unit_cost = models.DecimalField(
#         max_digits=19, decimal_places=10, default=0)
#     retail_price = models.DecimalField(
#         max_digits=19, decimal_places=10, default=1)

#     def __str__(self):
#         return f"{ self.name }"


# class SalesOrder(models.Model):
#     created_date = models.DateField(default=date.today)
#     invoice_date = models.DateField(default=date.today)
#     invoice_number = models.IntegerField()
#     reference = models.CharField(max_length=32)
#     customer = models.ForeignKey(
#         Customer, on_delete=models.CASCADE, related_name="orders")
#     status = models.CharField(max_length=32, choices=STATUS_CHOICES)
#     saleschannel = models.ForeignKey(SalesChannel, on_delete=models.PROTECT)
#     warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order No. { self.id } with Ref { self.reference }"


# class Item(models.Model):
#     order = models.ForeignKey(
#         SalesOrder, on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey(Product, on_delete=models.PROTECT)
#     quantity = models.DecimalField(
#         max_digits=19, decimal_places=10, default=1)
#     price = models.DecimalField(
#         max_digits=19, decimal_places=10, default=1)
#     discount = models.DecimalField(max_digits=3, decimal_places=2, default=0)

#     def sub_total(self):
#         return self.quantity * (1 - self.discount) * self.price

#     def __str__(self):
#         return f"Item: { self.quantity } x { self.product }"


# class Shelf(models.Model):
#     warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.DecimalField(
#         max_digits=19, decimal_places=10, default=1)
