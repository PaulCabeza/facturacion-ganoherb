# Generated by Django 5.1.2 on 2024-11-06 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'blank': 'El nombre del cliente es requerido', 'null': 'El nombre del cliente es requerido'}, max_length=200, verbose_name='Nombre')),
                ('code_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='Código de distribuidor')),
                ('email', models.EmailField(error_messages={'blank': 'El correo electrónico es requerido', 'invalid': 'Ingrese un correo electrónico válido', 'null': 'El correo electrónico es requerido', 'unique': 'Ya existe un cliente con este correo electrónico'}, max_length=254, unique=True, verbose_name='Correo electrónico')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Teléfono')),
                ('address', models.TextField(blank=True, verbose_name='Dirección')),
                ('nit', models.CharField(error_messages={'blank': 'El NIT es requerido', 'null': 'El NIT es requerido'}, max_length=20, verbose_name='NIT')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'blank': 'El nombre del producto es requerido', 'null': 'El nombre del producto es requerido'}, max_length=200, verbose_name='Nombre')),
                ('units_per_box', models.IntegerField(error_messages={'invalid': 'Ingrese un número válido', 'null': 'La cantidad de unidades por caja es requerida'}, verbose_name='Unidades por caja')),
                ('distributor_price', models.DecimalField(decimal_places=2, error_messages={'invalid': 'Ingrese un precio válido', 'null': 'El precio distribuidor es requerido'}, max_digits=10, verbose_name='Precio distribuidor')),
                ('public_price', models.DecimalField(decimal_places=2, error_messages={'invalid': 'Ingrese un precio válido', 'null': 'El precio público es requerido'}, max_digits=10, verbose_name='Precio público')),
                ('quantity', models.IntegerField(error_messages={'invalid': 'Ingrese una cantidad válida', 'null': 'La cantidad es requerida'}, verbose_name='Cantidad')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(error_messages={'blank': 'El número de factura es requerido', 'null': 'El número de factura es requerido', 'unique': 'Ya existe una factura con este número'}, max_length=20, unique=True, verbose_name='Número de factura')),
                ('date', models.DateTimeField(error_messages={'invalid': 'Ingrese una fecha válida', 'null': 'La fecha es requerida'}, verbose_name='Fecha')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total')),
                ('paid', models.BooleanField(default=False, verbose_name='Pagada')),
                ('customer', models.ForeignKey(error_messages={'null': 'Debe seleccionar un cliente'}, on_delete=django.db.models.deletion.CASCADE, to='inventory.customer', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
            },
        ),
        migrations.CreateModel(
            name='InvoiceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='inventory.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.product')),
            ],
            options={
                'verbose_name': 'Detalle de Factura',
                'verbose_name_plural': 'Detalles de Factura',
            },
        ),
    ]
