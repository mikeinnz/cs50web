from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Shelf)
