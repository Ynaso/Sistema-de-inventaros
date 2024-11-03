from django.db import models
from productos.models import Producto

from django.db.models import Sum, F

class TipoMovimiento(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

from django.db import models
from productos.models import Producto
from django.db.models import Sum, F
from decimal import Decimal  # Import Decimal

class Kardex(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.ForeignKey('TipoMovimiento', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.PositiveIntegerField()

    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    total_valor = models.DecimalField(max_digits=15, decimal_places=2)

    referencia_factura_venta = models.ForeignKey(
        'ventas.FacturaVenta', on_delete=models.SET_NULL, null=True, blank=True
    )
    referencia_factura_compra = models.ForeignKey(
        'compras.FacturaCompra', on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        """Override save() to ensure total_valor is calculated correctly."""
        # Calculate the new balance (saldo) based on the type of movement
        if self.tipo_movimiento.nombre == "Entrada":
            self.saldo = Kardex.calcular_saldo(self.producto) + self.cantidad
        else:
            self.saldo = Kardex.calcular_saldo(self.producto) - self.cantidad

        # Ensure all calculations use Decimal to avoid type errors
        self.total_valor = Decimal(self.saldo) * Decimal(self.costo_unitario)

        # Call the parent class's save method
        super().save(*args, **kwargs)

    @classmethod
    def calcular_saldo(cls, producto):
        """Calculate the total stock (quantity in inventory) for a product."""
        entradas = cls.objects.filter(
            producto=producto, tipo_movimiento__nombre="Entrada"
        ).aggregate(total=Sum('cantidad'))['total'] or 0

        salidas = cls.objects.filter(
            producto=producto, tipo_movimiento__nombre="Salida"
        ).aggregate(total=Sum('cantidad'))['total'] or 0

        return entradas - salidas

    @classmethod
    def calcular_costo_promedio(cls, producto):
        """Calculate the weighted average cost for a product."""
        total_cost = cls.objects.filter(
            producto=producto, tipo_movimiento__nombre="Entrada"
        ).aggregate(
            total=Sum(F('costo_unitario') * F('cantidad'))
        )['total'] or Decimal(0)

        total_quantity = cls.objects.filter(
            producto=producto, tipo_movimiento__nombre="Entrada"
        ).aggregate(total=Sum('cantidad'))['total'] or 0

        if total_quantity == 0:
            return Decimal(0)  # Avoid division by zero

        return total_cost / Decimal(total_quantity)

