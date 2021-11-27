from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('customer/new', views.create_customer, name="create_customer"),
    path('customer/list', views.list_customer, name="list_customer"),
    path('customer/edit/<int:id>', views.edit_customer, name="edit_customer"),
    path('warehouse/list', views.warehouse, name="warehouse"),
    path('warehouse/new', views.create_warehouse, name="create_warehouse"),
    path('warehouse/edit/<int:id>', views.edit_warehouse, name="edit_warehouse"),
]
