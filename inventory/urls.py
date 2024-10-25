from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('distributors/', views.distributor_list, name='distributor_list'),
    path('invoices/', views.invoice_list, name='invoice_list'),
]
