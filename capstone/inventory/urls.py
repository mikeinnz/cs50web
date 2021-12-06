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
    path('warehouse/view/<int:id>', views.view_warehouse, name="view_warehouse"),
    path('warehouse/<int:id>', views.warehouse_api, name="warehouse_api"),
    path('product/list', views.product, name="product"),
    path('product/new', views.create_product, name="create_product"),
    path('product/edit/<int:id>', views.edit_product, name="edit_product"),
    path('category/new', views.create_category, name="create_category"),
    path('category/edit/<int:id>', views.edit_category, name="edit_category"),
    path('order/list', views.order, name="order"),
    path('order/new', views.create_order, name="create_order"),
    path('order/edit/<int:id>', views.edit_order, name="edit_order"),
    #path('order/api', views.order_api, name="order_api"),
    path('channel/new', views.create_sales_channel, name="create_sales_channel"),
    path('channel/edit/<int:id>', views.edit_sales_channel,
         name="edit_sales_channel"),
]
