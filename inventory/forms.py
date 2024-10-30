from django import forms
from django.utils import timezone
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = timezone.now()
        

class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = ['product', 'quantity', 'unit_price', 'subtotal']
        widgets = {
            'subtotal': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        if quantity and unit_price:
            cleaned_data['subtotal'] = quantity * unit_price
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({'class': 'w-16 text-sm px-2 py-1 border rounded'})
        self.fields['unit_price'].widget.attrs.update({'class': 'w-16 text-sm px-2 py-1 border rounded'})
        self.fields['subtotal'].widget.attrs.update({'class': 'w-20 text-sm px-2 py-1 border rounded'})