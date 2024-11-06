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
    InvoiceDetailFormSet = inlineformset_factory(
        Invoice, 
        InvoiceDetail, 
        form=InvoiceDetailForm, 
        extra=1,
        can_delete=True
    )
    
    if request.method == 'POST':
        print("\n=== DEBUG POST DATA ===")
        for key, value in request.POST.items():
            print(f"{key}: {value}")
        print("======================\n")
        
        form = InvoiceForm(request.POST)
        
        # Obtener el número total de formularios
        total_forms = int(request.POST.get('form-TOTAL_FORMS', 0))
        print(f"Total forms received: {total_forms}")
        
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.total = 0
            invoice.save()
            
            total = 0
            details_to_save = []
            
            # Procesar cada formulario
            for i in range(total_forms):
                product_id = request.POST.get(f'form-{i}-product')
                quantity = request.POST.get(f'form-{i}-quantity')
                unit_price = request.POST.get(f'form-{i}-unit_price')
                
                print(f"\nProcessing form {i}:")
                print(f"Product ID: {product_id}")
                print(f"Quantity: {quantity}")
                print(f"Unit Price: {unit_price}")
                
                # Verificar si todos los campos necesarios están presentes
                if product_id and quantity and unit_price and product_id != 'None':
                    try:
                        product = Product.objects.get(pk=product_id)
                        quantity = int(quantity)
                        unit_price = float(unit_price)
                        
                        print(f"Found product: {product.name}")
                        print(f"Current stock: {product.quantity}")
                        
                        # Verificar stock
                        if product.quantity < quantity:
                            error_msg = f"No hay suficiente stock del producto {product.name}. Stock actual: {product.quantity}"
                            print(f"Error: {error_msg}")
                            invoice.delete()
                            return render(request, 'inventory/invoice_form.html', {
                                'form': form,
                                'formset': InvoiceDetailFormSet(request.POST),
                                'form_errors': [error_msg]
                            })
                        
                        # Crear detalle
                        subtotal = quantity * unit_price
                        detail = InvoiceDetail(
                            invoice=invoice,
                            product=product,
                            quantity=quantity,
                            unit_price=unit_price,
                            subtotal=subtotal
                        )
                        details_to_save.append(detail)
                        total += subtotal
                        
                        print(f"Detail created - Subtotal: {subtotal}")
                        
                    except Product.DoesNotExist:
                        print(f"Error: Product with ID {product_id} not found")
                    except ValueError as e:
                        print(f"Error converting values: {e}")
            
            if not details_to_save:
                error_msg = "Debe agregar al menos un producto a la factura"
                print(f"\nError: {error_msg}")
                invoice.delete()
                return render(request, 'inventory/invoice_form.html', {
                    'form': form,
                    'formset': InvoiceDetailFormSet(request.POST),
                    'form_errors': [error_msg]
                })
            
            print(f"\nSaving {len(details_to_save)} details")
            
            # Guardar todos los detalles y actualizar stock
            for detail in details_to_save:
                # Actualizar stock
                detail.product.quantity -= detail.quantity
                detail.product.save()
                # Guardar detalle
                detail.save()
                print(f"Saved detail for product {detail.product.name}")
                print(f"Updated stock: {detail.product.quantity}")
            
            # Actualizar el total de la factura
            invoice.total = total
            invoice.save()
            print(f"\nInvoice saved with total: {total}")
            
            return redirect('inventory:invoice_print', pk=invoice.pk)
        else:
            print("\nForm errors:", form.errors)
            return render(request, 'inventory/invoice_form.html', {
                'form': form,
                'formset': InvoiceDetailFormSet(request.POST),
                'form_errors': form.errors
            })
    else:
        form = InvoiceForm(initial={'date': timezone.now()})
        formset = InvoiceDetailFormSet()
    
    return render(request, 'inventory/invoice_form.html', {
        'form': form, 
        'formset': formset,
        'form_errors': []
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

@login_required
def validate_invoice_number(request):
    invoice_number = request.GET.get('invoice_number', '')
    exists = Invoice.objects.filter(invoice_number=invoice_number).exists()
    return JsonResponse({'exists': exists})

def access_denied(request):
    return render(request, 'inventory/access_denied.html')
