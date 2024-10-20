from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Product, Customer, Invoice
from .forms import ProductForm  # Necesitarás crear este formulario

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('inventory:index')

@login_required
def index(request):
    return render(request, 'inventory/index.html')

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'inventory/customer_list.html', {'customers': customers})

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'inventory/invoice_list.html', {'invoices': invoices})

# Implementa estas vistas más adelante
# def product_update(request, pk):
#     pass

# def product_delete(request, pk):
#     pass
