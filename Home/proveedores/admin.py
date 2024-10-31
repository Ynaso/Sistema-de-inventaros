from django.contrib import admin
from .models import Proveedor, TipoCompra

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_proveedor', 'estado', 'numero_ruc')
    search_fields = ('nombre', 'numero_ruc')
    list_filter = ('tipo_proveedor', 'estado')

@admin.register(TipoCompra)
class TipoCompraAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
