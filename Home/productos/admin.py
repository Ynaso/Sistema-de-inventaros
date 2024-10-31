from django.contrib import admin
from .models import Producto, Categoria, EstadoProducto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre', 'categoria', 'estado')
    search_fields = ('nombre', 'codigo')
    list_filter = ('categoria', 'estado')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(EstadoProducto)
class EstadoProductoAdmin(admin.ModelAdmin):
    list_display = ('estado',)
