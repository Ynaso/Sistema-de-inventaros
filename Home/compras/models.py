from django.db import models
from django.db.models.signals import post_save
from decimal import Decimal
from django.dispatch import receiver
from productos.models import Producto
from kardex.models import TipoMovimiento, Kardex  # Ensure these imports are correct

class FacturaCompra(models.Model):
    proveedor = models.ForeignKey('proveedores.Proveedor', on_delete=models.CASCADE)  # Use string reference
    fecha_ingreso = models.DateField()
    responsable = models.CharField(max_length=100)

    def __str__(self):
        return f"Factura Compra {self.id}"

class DetalleCompra(models.Model):
    factura = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Compra {self.factura.id} - {self.producto.nombre}"

@receiver(post_save, sender=DetalleCompra)
def create_kardex_entry(sender, instance, created, **kwargs):
    if created:
        # Get or create the "Entrada" movement type
        tipo_movimiento, _ = TipoMovimiento.objects.get_or_create(nombre="Entrada")

        # Calculate the current stock balance BEFORE the new entry
        saldo_actual = Kardex.calcular_saldo(instance.producto)

        # Calculate the current weighted average cost
        costo_promedio_actual = Kardex.calcular_costo_promedio(instance.producto)

        # Debug: Print current state to track values
        print(f"Saldo Actual: {saldo_actual}")
        print(f"Costo Promedio Actual: {costo_promedio_actual}")

        # Handle the first entry: if no existing stock, use the new cost directly
        if saldo_actual == 0:
            costo_promedio_final = Decimal(instance.costo_unitario)
        else:
            # Calculate the total costs for existing and new stock
            total_cost_existing = Decimal(saldo_actual) * Decimal(costo_promedio_actual)
            total_cost_new = Decimal(instance.cantidad) * Decimal(instance.costo_unitario)

            # New weighted average = (Existing cost + New cost) / Total quantity
            costo_promedio_final = (total_cost_existing + total_cost_new) / (saldo_actual + instance.cantidad)

        # Debug: Print final cost to confirm correct calculation
        print(f"Costo Promedio Final: {costo_promedio_final}")

        # Create a new Kardex entry with the updated information
        Kardex.objects.create(
            producto=instance.producto,
            tipo_movimiento=tipo_movimiento,
            cantidad=instance.cantidad,
            saldo=saldo_actual + instance.cantidad,
            costo_unitario=costo_promedio_final,  # Use the recalculated average cost
            precio_venta=instance.precio_unitario,  # Use the sale price from purchase detail
            referencia_factura_compra=instance.factura,  # Reference to purchase invoice
        )
