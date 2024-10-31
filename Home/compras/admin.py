from django.contrib import admin
from .models import FacturaCompra, DetalleCompra

@admin.register(FacturaCompra)
class FacturaCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha_ingreso', 'responsable')
    search_fields = ('id',)
    list_filter = ('fecha_ingreso',)

@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'cantidad', 'precio_unitario')

#@admin.register(DevolucionCompra)
#class DevolucionCompraAdmin(admin.ModelAdmin):
#   list_display = ('factura_compra', 'producto', 'cantidad_devuelta', 'fecha_devolucion')
