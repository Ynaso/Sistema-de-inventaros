from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from productos.models import Producto
from clientes.models import Cliente
from kardex.models import TipoMovimiento, Kardex  # Verifica que esta importación sea correcta

class TipoVenta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class FacturaVenta(models.Model):
    numero_factura = models.AutoField(primary_key=True)  # Cambiado a AutoField
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_salida = models.DateField()
    tipo_venta = models.ForeignKey(TipoVenta, on_delete=models.CASCADE)

    def __str__(self):
        return f"Factura {self.numero_factura}"

class DetalleVenta(models.Model):
    factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE, related_name='detalles')  # Agregado related_name
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.factura.numero_factura} - {self.producto.nombre}"
    


class DevolucionVenta(models.Model):
    factura_venta = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE, related_name='devoluciones')  # Agregado related_name
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_devuelta = models.PositiveIntegerField()
    fecha_devolucion = models.DateField()

    def __str__(self):
        return f"Devolución {self.factura_venta.numero_factura} - {self.producto.nombre}"

# Señal para actualizar Kardex con la salida de inventario en una venta
@receiver(post_save, sender=DetalleVenta)
def create_kardex_entry_sale(sender, instance, created, **kwargs):
    if created:
        # Obtener o crear el tipo de movimiento "Salida" para la venta
        tipo_movimiento, _ = TipoMovimiento.objects.get_or_create(nombre="Salida")

        # Obtener el saldo actual antes de la venta
        saldo_actual = Kardex.calcular_saldo(instance.producto)

        # Verificar que el inventario actual sea suficiente para la venta
        if Decimal(saldo_actual) < Decimal(instance.cantidad):
            raise ValueError("No hay suficiente inventario para realizar esta venta.")

        # Calcular el costo promedio actual
        costo_promedio_actual = Kardex.calcular_costo_promedio(instance.producto)

        # Saldo final después de la venta (restar la cantidad vendida)
        saldo_final = Decimal(saldo_actual) - (Decimal(instance.cantidad))
        print(f"el saldo actual al realizar la venta es {saldo_actual}")
        print(f"la cantidad a restar a el saldo actual es {-1* Decimal(instance.cantidad)}")

        # Crear un nuevo registro en el Kardex para registrar la salida
        Kardex.objects.create(
            producto=instance.producto,
            tipo_movimiento=tipo_movimiento,
            cantidad = Decimal(instance.cantidad),  # Cantidad negativa para salida
            saldo=saldo_final,
            costo_unitario=costo_promedio_actual,  # Usamos el costo promedio actual
            precio_venta=instance.precio_venta,  # Precio de venta registrado
            referencia_factura_venta=instance.factura,  # Referencia a la factura de venta
        )

        # Debug para confirmar la salida en Kardex
        print(f"Venta registrada en Kardex: Producto {instance.producto.nombre}, Cantidad salida {instance.cantidad}, Saldo final {saldo_final}")
