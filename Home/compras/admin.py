from django.contrib import admin
from .models import FacturaCompra, DetalleCompra, TipoCompra

@admin.register(FacturaCompra)
class FacturaCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha_ingreso', 'responsable')
    search_fields = ('id',)
    list_filter = ('fecha_ingreso',)

@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'cantidad', 'precio_unitario')

class TipoCompraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')  # Fields to display in the list view
    search_fields = ('nombre',)  # Allow searching by 'nombre'
    ordering = ('nombre',)  # Order by 'nombre' by default

admin.site.register(TipoCompra, TipoCompraAdmin)

#@admin.register(DevolucionCompra)
#class DevolucionCompraAdmin(admin.ModelAdmin):
#   list_display = ('factura_compra', 'producto', 'cantidad_devuelta', 'fecha_devolucion')
