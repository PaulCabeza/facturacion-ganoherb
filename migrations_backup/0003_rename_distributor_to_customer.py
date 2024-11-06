from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20240000_0000'),  # Ajusta esto al número de tu última migración
    ]

    operations = [
        # Primero renombramos la tabla
        migrations.RenameModel(
            old_name='Distributor',
            new_name='Customer',
        ),
        # Luego actualizamos el campo en Invoice
        migrations.RenameField(
            model_name='invoice',
            old_name='customer',
            new_name='customer',
        ),
        # Actualizamos las opciones del modelo
        migrations.AlterModelOptions(
            name='Customer',
            options={'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
        # Hacemos opcional el campo code_id
        migrations.AlterField(
            model_name='Customer',
            name='code_id',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=10,
                verbose_name='Código de distribuidor'
            ),
        ),
    ] 