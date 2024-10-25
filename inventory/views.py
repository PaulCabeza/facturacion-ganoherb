from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.http import JsonResponse
from .models import Product, Distributor, Invoice, InvoiceDetail
from .forms import ProductForm, DistributorForm, InvoiceForm, InvoiceDetailForm

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
def distributor_create(request):
    if request.method == 'POST':
        form = DistributorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:distributor_list')
    else:
        form = DistributorForm()
    return render(request, 'inventory/distributor_form.html', {'form': form})

@login_required
def distributor_update(request, pk):
    distributor = get_object_or_404(Distributor, pk=pk)
    if request.method == 'POST':
        form = DistributorForm(request.POST, instance=distributor)
        if form.is_valid():
            form.save()
            return redirect('inventory:distributor_list')
    else:
        form = DistributorForm(instance=distributor)
    return render(request, 'inventory/distributor_form.html', {'form': form, 'distributor': distributor})

@login_required
def distributor_delete(request, pk):
    pass

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'inventory/invoice_list.html', {'invoices': invoices})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'inventory/invoice_detail.html', {'invoice': invoice})

@login_required
def invoice_create(request):
    InvoiceDetailFormSet = inlineformset_factory(Invoice, InvoiceDetail, form=InvoiceDetailForm, extra=1)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceDetailFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.instance = invoice
            formset.save()
            return redirect('inventory:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
        formset = InvoiceDetailFormSet()
    
    return render(request, 'inventory/invoice_form.html', {'form': form, 'formset': formset})

@login_required
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    InvoiceDetailFormSet = inlineformset_factory(Invoice, InvoiceDetail, form=InvoiceDetailForm, extra=1)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceDetailFormSet(request.POST, instance=invoice)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('inventory:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceDetailFormSet(instance=invoice)
    
    return render(request, 'inventory/invoice_form.html', {'form': form, 'formset': formset, 'invoice': invoice})

@login_required
def get_distributor_details(request, pk):
    distributor = get_object_or_404(Distributor, pk=pk)
    data = {
        'code_id': distributor.code_id,
        'address': distributor.address,
        'phone': distributor.phone,
    }
    return JsonResponse(data)

@login_required
def invoice_print(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'inventory/invoice_print.html', {'invoice': invoice})

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

