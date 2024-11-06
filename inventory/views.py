from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from django.db import transaction
from .models import Product, Distributor, Invoice, InvoiceDetail
from .forms import ProductForm, DistributorForm, InvoiceForm, InvoiceDetailForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('inventory:index')

@login_required
def index(request):
    # Obtener los últimos 5 registros de cada modelo
    products = Product.objects.all().order_by('-id')[:5]
    distributors = Distributor.objects.all().order_by('-id')[:5]
    invoices = Invoice.objects.all().order_by('-date')[:5]

    context = {
        'total_products': Product.objects.count(),
        'total_distributors': Distributor.objects.count(),
        'total_invoices': Invoice.objects.count(),
        'products': products,
        'distributors': distributors,
        'invoices': invoices,
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
            # Guardar sin validaciones adicionales
            product = form.save(commit=False)
            product.save()
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
@transaction.atomic
def invoice_create(request):
    InvoiceDetailFormSet = inlineformset_factory(Invoice, InvoiceDetail, form=InvoiceDetailForm, extra=1)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceDetailFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.total = 0
            invoice.save()
            
            formset.instance = invoice
            details = formset.save(commit=False)
            
            if not details:  # Si no hay detalles
                form.add_error(None, "Debe agregar al menos un producto a la factura")
                invoice.delete()
            else:
                total = 0
                # Verificar stock y actualizar inventario
                for detail in details:
                    product = detail.product
                    if product.quantity < detail.quantity:
                        form.add_error(None, f"No hay suficiente stock del producto {product.name}. Stock actual: {product.quantity}")
                        invoice.delete()
                        return render(request, 'inventory/invoice_form.html', {
                            'form': form,
                            'formset': formset,
                            'form_errors': form.errors.get('__all__', [])
                        })
                    
                    # Actualizar el stock
                    product.quantity -= detail.quantity
                    product.save()
                    
                    # Calcular subtotal y guardar detalle
                    detail.subtotal = detail.quantity * detail.unit_price
                    total += detail.subtotal
                    detail.save()
                
                # Actualizar el total de la factura
                invoice.total = total
                invoice.save()
                
                return redirect('inventory:invoice_print', pk=invoice.pk)
    else:
        form = InvoiceForm(initial={'date': timezone.now()})
        formset = InvoiceDetailFormSet()
    
    return render(request, 'inventory/invoice_form.html', {
        'form': form, 
        'formset': formset,
        'form_errors': form.errors.get('__all__', [])
    })

@login_required
@transaction.atomic
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    InvoiceDetailFormSet = inlineformset_factory(Invoice, InvoiceDetail, form=InvoiceDetailForm, extra=1)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceDetailFormSet(request.POST, instance=invoice)
        
        if form.is_valid() and formset.is_valid():
            # Restaurar el inventario anterior
            for detail in invoice.details.all():
                product = detail.product
                product.quantity += detail.quantity
                product.save()
            
            invoice = form.save(commit=False)
            details = formset.save(commit=False)
            
            if not details:
                form.add_error(None, "Debe agregar al menos un producto a la factura")
            else:
                total = 0
                # Verificar stock y actualizar inventario
                for detail in details:
                    product = detail.product
                    if product.quantity < detail.quantity:
                        form.add_error(None, f"No hay suficiente stock del producto {product.name}. Stock actual: {product.quantity}")
                        return render(request, 'inventory/invoice_form.html', {
                            'form': form,
                            'formset': formset,
                            'invoice': invoice,
                            'form_errors': form.errors.get('__all__', [])
                        })
                    
                    # Actualizar el stock
                    product.quantity -= detail.quantity
                    product.save()
                    
                    # Calcular subtotal y guardar detalle
                    detail.subtotal = detail.quantity * detail.unit_price
                    total += detail.subtotal
                    detail.save()
                
                # Actualizar el total de la factura
                invoice.total = total
                invoice.save()
                
                return redirect('inventory:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceDetailFormSet(instance=invoice)
    
    return render(request, 'inventory/invoice_form.html', {
        'form': form,
        'formset': formset,
        'invoice': invoice
    })

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
            # Guardar sin validaciones adicionales
            product = form.save(commit=False)
            product.save()
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
