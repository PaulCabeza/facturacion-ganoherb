from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Product, Distributor, Invoice
from .forms import ProductForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('inventory:index')

@login_required
def index(request):
    total_products = Product.objects.count()
    products = Product.objects.all()
    context = {
        'total_products': total_products,
        'products': products,
    }
    return render(request, 'inventory/index.html', context)

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
def distributor_list(request):
    distributors = Distributor.objects.all()
    return render(request, 'inventory/distributor_list.html', {'distributors': distributors})

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'inventory/invoice_list.html', {'invoices': invoices})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'product': product})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('inventory:product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})

# Implementa estas vistas más adelante
# def product_update(request, pk):
#     pass

# def product_delete(request, pk):
#     pass
