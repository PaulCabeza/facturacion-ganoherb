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

class Distributor(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre",
        error_messages={
            'blank': 'El nombre del distribuidor es requerido',
            'null': 'El nombre del distribuidor es requerido',
        }
    )
    code_id = models.CharField(
        max_length=10,
        verbose_name="Código",
        error_messages={
            'blank': 'El código es requerido',
            'null': 'El código es requerido',
        }
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico",
        error_messages={
            'unique': 'Ya existe un distribuidor con este correo electrónico',
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

    class Meta:
        verbose_name = "Distribuidor"
        verbose_name_plural = "Distribuidores"

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
        Distributor,
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
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name="Factura"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Producto",
        error_messages={
            'null': 'Debe seleccionar un producto',
        }
    )
    quantity = models.IntegerField(
        verbose_name="Cantidad",
        error_messages={
            'invalid': 'Ingrese una cantidad válida',
            'null': 'La cantidad es requerida',
        }
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio unitario",
        error_messages={
            'invalid': 'Ingrese un precio válido',
            'null': 'El precio unitario es requerido',
        }
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Subtotal"
    )

    class Meta:
        verbose_name = "Detalle de factura"
        verbose_name_plural = "Detalles de factura"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
