# kardex/admin.py
from django.contrib import admin
from .models import Kardex, TipoMovimiento

@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(admin.ModelAdmin):
    """Admin configuration for TipoMovimiento."""
    list_display = ('id', 'nombre')  # Display the ID and name
    search_fields = ('nombre',)  # Allow searching by name

@admin.register(Kardex)
class KardexAdmin(admin.ModelAdmin):
    """Admin configuration for Kardex."""
    list_display = (
        'id', 'producto', 'fecha_movimiento', 'tipo_movimiento', 
        'cantidad', 'saldo', 'costo_unitario', 'precio_venta', 'total_valor',
        'referencia_factura_compra', 'referencia_factura_venta'
    )  # Show all necessary fields

    search_fields = ('producto__nombre',)  # Enable search by product name
    list_filter = ('tipo_movimiento', 'fecha_movimiento')  # Enable filtering by movement type and date
    date_hierarchy = 'fecha_movimiento'  # Add a date hierarchy for easy browsing

    # Optionally, make some fields read-only to prevent modification in the admin
    readonly_fields = (
        'producto', 'fecha_movimiento', 'tipo_movimiento', 
        'cantidad', 'saldo', 'costo_unitario', 'precio_venta', 
        'referencia_factura_compra', 'referencia_factura_venta'
    )

    fieldsets = (
        (None, {
            'fields': (
                'producto', 'fecha_movimiento', 'tipo_movimiento', 
                'cantidad', 'saldo', 'costo_unitario', 'precio_venta',
                'referencia_factura_compra', 'referencia_factura_venta'
            ),
        }),
    )
