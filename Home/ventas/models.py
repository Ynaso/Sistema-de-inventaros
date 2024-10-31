from django.db import models
from productos.models import Producto
from clientes.models import Cliente

class TipoVenta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class FacturaVenta(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_salida = models.DateField()
    tipo_venta = models.ForeignKey(TipoVenta, on_delete=models.CASCADE)

    def __str__(self):
        return f"Factura {self.numero_factura}"

class DetalleVenta(models.Model):
    factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.factura.numero_factura} - {self.producto.nombre}"

class DevolucionVenta(models.Model):
    factura_venta = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_devuelta = models.PositiveIntegerField()
    fecha_devolucion = models.DateField()
