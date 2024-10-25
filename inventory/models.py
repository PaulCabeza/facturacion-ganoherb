from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)    
    units_per_box = models.IntegerField()
    distributor_price = models.DecimalField(max_digits=10, decimal_places=2)
    public_price = models.DecimalField(max_digits=10, decimal_places=2)    
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

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
    customer = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.id} - {self.customer.name}"

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
