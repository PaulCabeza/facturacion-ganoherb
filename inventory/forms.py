from django import forms
from .models import Product, Distributor, Invoice, InvoiceDetail

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'units_per_box', 'distributor_price', 'public_price', 'quantity']
        labels = {
            'name': 'Nombre',
            'units_per_box': 'Sobres por caja',
            'distributor_price': 'Precio distribuidor',
            'public_price': 'Precio al público',
            'quantity': 'Cantidad',
        }


class DistributorForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = ['name', 'code_id', 'nit', 'phone', 'email', 'address']
        labels = {
            'name': 'Nombre',
            'code_id': 'Código de distribuidor',
            'nit': 'NIT',
            'phone': 'Teléfono',
            'email': 'Correo electrónico',
            'address': 'Dirección',            
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'customer', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = ['product', 'quantity', 'unit_price']
