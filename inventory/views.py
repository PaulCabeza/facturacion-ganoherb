from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from django.db import transaction
from .models import Product, Customer, Invoice, InvoiceDetail
from .forms import ProductForm, CustomerForm, InvoiceForm, InvoiceDetailForm
from django.core.exceptions import ValidationError

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('inventory:index')

@login_required
def index(request):
    # Obtener los últimos 5 registros de cada modelo
    products = Product.objects.all().order_by('-id')[:5]
    customers = Customer.objects.all().order_by('-id')[:5]
    invoices = Invoice.objects.all().order_by('-date')[:5]

    context = {
        'total_products': Product.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_invoices': Invoice.objects.count(),
        'products': products,
        'customers': customers,
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
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'inventory/customer_list.html', {'customers': customers})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'inventory/customer_form.html', {'form': form})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('inventory:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'inventory/customer_form.html', {'form': form, 'customer': customer})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('inventory:customer_list')
    return render(request, 'inventory/customer_confirm_delete.html', {'customer': customer})

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
        form = InvoiceForm(request.POST)
        formset = InvoiceDetailFormSet(request.POST)
        
        # Validación manual del tipo de factura y número de registro
        invoice_type = request.POST.get('type')
        customer_id = request.POST.get('customer')
        
        try:
            customer = Customer.objects.get(pk=customer_id) if customer_id else None
            if invoice_type == 'CCF' and customer and not customer.registration_number:
                return render(request, 'inventory/invoice_form.html', {
                    'form': form,
                    'formset': formset,
                    'form_errors': ['Para Comprobante de Crédito Fiscal, el cliente debe tener número de registro'],
                    'formatted_date': request.POST.get('date')
                })
        except Customer.DoesNotExist:
            pass
        
        # Continuar con la validación normal del formulario
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.type = invoice_type  # Asegurarnos de guardar el tipo de factura
            invoice.total = 0
            invoice.save()
            
            # Obtener el número total de formularios
            total_forms = int(request.POST.get('form-TOTAL_FORMS', 0))
            
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
                                'formset': formset,
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
                    'formset': formset,
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
                'formset': formset,
                'form_errors': form.errors,
                'formatted_date': request.POST.get('date')
            })
    else:
        form = InvoiceForm(initial={'date': timezone.now()})
        formset = InvoiceDetailFormSet()
    
    return render(request, 'inventory/invoice_form.html', {
        'form': form,
        'formset': formset,
        'form_errors': [],
        'is_update': False,
        'formatted_date': timezone.now().strftime('%Y-%m-%dT%H:%M')
    })

@login_required
@transaction.atomic
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    InvoiceDetailFormSet = inlineformset_factory(
        Invoice, 
        InvoiceDetail, 
        form=InvoiceDetailForm, 
        extra=0,
        can_delete=True
    )
    
    formatted_date = invoice.date.strftime('%Y-%m-%dT%H:%M') if invoice.date else None
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceDetailFormSet(request.POST, instance=invoice)
        
        # Validación manual del tipo de factura y número de registro
        invoice_type = request.POST.get('type')
        customer_id = request.POST.get('customer')
        
        try:
            customer = Customer.objects.get(pk=customer_id) if customer_id else None
            if invoice_type == 'CCF' and customer and not customer.registration_number:
                return render(request, 'inventory/invoice_form.html', {
                    'form': form,
                    'formset': formset,
                    'form_errors': ['Para Comprobante de Crédito Fiscal, el cliente debe tener número de registro'],
                    'invoice': invoice,
                    'formatted_date': formatted_date,
                    'is_update': True
                })
        except Customer.DoesNotExist:
            pass
            
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Actualizar la factura principal
                    invoice.invoice_number = request.POST.get('invoice_number')
                    invoice.date = request.POST.get('date')
                    invoice.customer_id = request.POST.get('customer')
                    invoice.type = invoice_type  # Asegurarnos de guardar el tipo de factura
                    invoice.save()
                    
                    # Restaurar el inventario anterior
                    for detail in invoice.details.all():
                        product = detail.product
                        product.quantity += detail.quantity
                        product.save()
                        print(f"Restored stock for {product.name}: {product.quantity}")
                    
                    # Eliminar todos los detalles anteriores
                    invoice.details.all().delete()
                    
                    # Procesar los nuevos detalles
                    total = 0
                    total_forms = int(request.POST.get('form-TOTAL_FORMS', 0))
                    
                    for i in range(total_forms):
                        product_id = request.POST.get(f'form-{i}-product')
                        quantity = request.POST.get(f'form-{i}-quantity')
                        unit_price = request.POST.get(f'form-{i}-unit_price')
                        
                        if product_id and quantity and unit_price and product_id != 'None':
                            product = Product.objects.get(pk=product_id)
                            quantity = int(quantity)
                            unit_price = float(unit_price)
                            
                            # Verificar stock
                            if product.quantity < quantity:
                                raise ValidationError(f"No hay suficiente stock del producto {product.name}. Stock actual: {product.quantity}")
                            
                            # Crear detalle
                            subtotal = quantity * unit_price
                            detail = InvoiceDetail.objects.create(
                                invoice=invoice,
                                product=product,
                                quantity=quantity,
                                unit_price=unit_price,
                                subtotal=subtotal
                            )
                            
                            # Actualizar stock
                            product.quantity -= quantity
                            product.save()
                            
                            total += subtotal
                            print(f"Saved detail: {product.name}, quantity: {quantity}, price: {unit_price}")
                    
                    if total == 0:
                        raise ValidationError("Debe agregar al menos un producto a la factura")
                    
                    # Actualizar el total de la factura
                    invoice.total = total
                    invoice.save()
                    
                    print(f"Invoice saved with total: {total}")
                    return redirect('inventory:invoice_detail', pk=invoice.pk)
            except ValidationError as e:
                return render(request, 'inventory/invoice_form.html', {
                    'form': form,
                    'formset': formset,
                    'invoice': invoice,
                    'form_errors': [str(e)],
                    'formatted_date': formatted_date,
                    'is_update': True
                })
        else:
            return render(request, 'inventory/invoice_form.html', {
                'form': form,
                'formset': formset,
                'invoice': invoice,
                'form_errors': form.errors,
                'formatted_date': formatted_date,
                'is_update': True
            })
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceDetailFormSet(instance=invoice)
    
    return render(request, 'inventory/invoice_form.html', {
        'form': form,
        'formset': formset,
        'invoice': invoice,
        'is_update': True,
        'formatted_date': formatted_date
    })

@login_required
def get_customer_details(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    data = {
        'code_id': customer.code_id,
        'address': customer.address,
        'phone': customer.phone,
        'registration_number': customer.registration_number,
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
