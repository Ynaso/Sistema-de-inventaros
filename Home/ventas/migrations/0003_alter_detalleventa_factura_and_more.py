# Generated by Django 4.1.3 on 2024-11-01 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_remove_facturaventa_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleventa',
            name='factura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='ventas.facturaventa'),
        ),
        migrations.AlterField(
            model_name='devolucionventa',
            name='factura_venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devoluciones', to='ventas.facturaventa'),
        ),
    ]
