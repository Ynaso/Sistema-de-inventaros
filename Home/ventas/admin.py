from django.contrib import admin
from .models import TipoVenta, FacturaVenta, DetalleVenta, DevolucionVenta

@admin.register(TipoVenta)
class TipoVentaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(FacturaVenta)
class FacturaVentaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'cliente', 'fecha_salida', 'tipo_venta')
    search_fields = ('numero_factura',)
    list_filter = ('tipo_venta', 'fecha_salida')

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'cantidad', 'precio_venta')

@admin.register(DevolucionVenta)
class DevolucionVentaAdmin(admin.ModelAdmin):
    list_display = ('factura_venta', 'producto', 'cantidad_devuelta', 'fecha_devolucion')
