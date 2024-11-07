from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(
        max_length=200, 
        verbose_name="Nombre",
        error_messages={
            'blank': 'El nombre del producto es requerido',
            'null': 'El nombre del producto es requerido',
        }
    )    
    units_per_box = models.IntegerField(
        verbose_name="Unidades por caja",
        error_messages={
            'invalid': 'Ingrese un número válido',
            'null': 'La cantidad de unidades por caja es requerida',
        }
    )
    distributor_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio distribuidor",
        error_messages={
            'invalid': 'Ingrese un precio válido',
            'null': 'El precio distribuidor es requerido',
        }
    )
    public_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio público",
        error_messages={
            'invalid': 'Ingrese un precio válido',
            'null': 'El precio público es requerido',
        }
    )    
    quantity = models.IntegerField(
        verbose_name="Cantidad",
        error_messages={
            'invalid': 'Ingrese una cantidad válida',
            'null': 'La cantidad es requerida',
        }
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre",
        error_messages={
            'blank': 'El nombre del cliente es requerido',
            'null': 'El nombre del cliente es requerido',
        }
    )
    code_id = models.CharField(
        max_length=10,
        verbose_name="Código de distribuidor",
        blank=True,  # Hacer opcional
        null=True,   # Hacer opcional
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico",
        error_messages={
            'unique': 'Ya existe un cliente con este correo electrónico',
            'invalid': 'Ingrese un correo electrónico válido',
            'blank': 'El correo electrónico es requerido',
            'null': 'El correo electrónico es requerido',
        }
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono"
    )
    address = models.TextField(
        blank=True,
        verbose_name="Dirección"
    )
    nit = models.CharField(
        max_length=20,
        verbose_name="NIT",
        error_messages={
            'blank': 'El NIT es requerido',
            'null': 'El NIT es requerido',
        }
    )
    registration_number = models.CharField(
        max_length=12,
        verbose_name="Número de registro",
        blank=True,
        null=True,
        error_messages={
            'blank': 'El número de registro es requerido',
            'null': 'El número de registro es requerido',
        }
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.name

class Invoice(models.Model):
    invoice_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de factura",
        error_messages={
            'unique': 'Ya existe una factura con este número',
            'blank': 'El número de factura es requerido',
            'null': 'El número de factura es requerido',
        }
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Cliente",
        error_messages={
            'null': 'Debe seleccionar un cliente',
        }
    )
    date = models.DateTimeField(
        verbose_name="Fecha",
        error_messages={
            'invalid': 'Ingrese una fecha válida',
            'null': 'La fecha es requerida',
        }
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Total"
    )
    paid = models.BooleanField(
        default=False,
        verbose_name="Pagada"
    )

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"Factura {self.invoice_number} - {self.customer.name}"

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.unit_price}"

    class Meta:
        verbose_name = "Detalle de Factura"
        verbose_name_plural = "Detalles de Factura"
