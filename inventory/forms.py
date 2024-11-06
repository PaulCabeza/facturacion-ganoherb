from django import forms
from .models import Product, Distributor, Invoice, InvoiceDetail

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'units_per_box', 'distributor_price', 'public_price', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
            'units_per_box': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
            'distributor_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600',
                'step': 'any'
            }),
            'public_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600',
                'step': 'any'
            }),
            'quantity': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
        }

class DistributorForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = ['name', 'code_id', 'email', 'phone', 'address', 'nit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
            'code_id': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600', 'rows': 3}),
            'nit': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'customer', 'date']
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
            'customer': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
            'date': forms.DateTimeInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600', 'type': 'datetime-local'}),
        }

class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = ['product', 'quantity', 'unit_price', 'subtotal']
        widgets = {
            'product': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600',
                'step': 'any'
            }),
            'subtotal': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-green-600', 'readonly': True}),
        }