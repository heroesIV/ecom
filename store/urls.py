from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
	# path('', home, name='home'),
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),

    path('update_item/', updateItem, name='update_item'),
    path('process_order/', processOrder, name='process_order'),

    path('products/', products, name='products'),
    path('add_product/', addProduct, name='addProduct'),
    path('update_product/<str:pk>/', updateProduct, name='updateProduct'),
    path('delete_product/<str:pk>/', deleteProduct, name='deleteProduct'),

    path('customers/', customers, name='customers'),
    path('add_customer/', addCustomer, name='addCustomer'),
    path('update_customer/<str:pk>/', updateCustomer, name='updateCustomer'),
    path('delete_customer/<str:pk>/', deleteCustomer, name='deleteCustomer'),

    path('dashboard/', dashboard, name='dashboard'),
    path('delivered_orders/', deliveredOrders, name='deliveredOrders'),
    path('update_order/<str:pk>/', updateOrder, name='updateOrder'),
    path('delete_order/<str:pk>/', deleteOrder, name='deleteOrder'),
    # path('confirm_order/', confirmOrder, name='confirm_order'),
    # path('order_status/', payment_status, name='order_status'),
]
