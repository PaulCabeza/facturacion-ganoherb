from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")    
    units_per_box = models.IntegerField(verbose_name="Unidades por caja")
    distributor_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio distribuidor"
    )
    public_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio público"
    )    
    quantity = models.IntegerField(verbose_name="Cantidad")

    def clean(self):
        # Eliminar cualquier validación personalizada que pudiera estar causando el problema
        pass

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class Distributor(models.Model):
    name = models.CharField(max_length=200)
    code_id = models.CharField(max_length=10, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    nit = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.invoice_number} - {self.customer.name}"

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
