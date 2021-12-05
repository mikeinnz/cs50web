from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(Shelf)
admin.site.register(SalesOrder)
admin.site.register(SalesItem)
admin.site.register(SalesChannel)
