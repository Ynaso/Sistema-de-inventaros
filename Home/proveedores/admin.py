from django.contrib import admin
from .models import Proveedor, TipoProveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_proveedor', 'estado', 'numero_ruc')
    search_fields = ('nombre', 'numero_ruc')
    list_filter = ('tipo_proveedor', 'estado')

@admin.register(TipoProveedor)
class TipoProveedor(admin.ModelAdmin):
    list_display = ('nombre',)
