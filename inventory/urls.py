from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('customers/', views.customer_list, name='customer_list'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
]
