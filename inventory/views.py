from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

@login_required
def index(request):
    return render(request, 'inventory/index.html')

@login_required
def product_list(request):
    # Implement product list view
    pass

@login_required
def customer_list(request):
    # Implement customer list view
    pass

@login_required
def invoice_list(request):
    # Implement invoice list view
    pass

@login_required
def create_invoice(request):
    # Implement create invoice view
    pass

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('inventory:index')
