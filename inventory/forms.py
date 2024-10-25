from django import forms
from .models import Product

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
