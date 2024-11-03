from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from .models import FacturaVenta, DetalleVenta, TipoVenta
from productos.models import Producto
from clientes.models import Cliente
from kardex.models import Kardex
from django.db.models import Sum, OuterRef, Subquery, F
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from .models import DetalleVenta

def formulario_venta(request):
    # Cargar datos necesarios para el formulario
  # Subconsulta para obtener el último registro de Kardex por producto
    kardex_subquery = Kardex.objects.filter(
        producto=OuterRef('pk')
    ).order_by('-fecha_movimiento')

    # Query para obtener productos con el último saldo, costo unitario y precio de venta
    productos = Producto.objects.annotate(
        stock=Subquery(kardex_subquery.values('saldo')[:1]),
        costo_unitario=Subquery(kardex_subquery.values('costo_unitario')[:1]),
        precio_venta=Subquery(kardex_subquery.values('precio_venta')[:1])
    )
    clientes = Cliente.objects.all()
    tipos_venta = TipoVenta.objects.all()

    # Renderizar el formulario con datos
    return render(request, "Ventas/factura_venta.html", {
        'productos': productos,
        'clientes': clientes,
        'tipos_venta': tipos_venta
    })

def detalle_ventas(request):
    # Query the DetalleVenta model
    detalles = DetalleVenta.objects.select_related('factura', 'producto').all()

    context = {
        'detalles': detalles  # Pass the queryset to the template
    }
    
    return render(request, 'Ventas/detalle_ventas.html', context)  # Update 'your_template.html' to your actual template name

@transaction.atomic
def procesar_venta(request):
    if request.method == "POST":
        print(request.POST)
        cliente_id = request.POST.get('cliente')
        tipo_venta_id = request.POST.get('tipo_venta')
        productos_ids = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')

        print(precios)
        
        # Crear la FacturaVenta
        factura_venta = FacturaVenta.objects.create(
            cliente_id=cliente_id,
            tipo_venta_id=tipo_venta_id,
            fecha_salida=timezone.now()
        )

        # Añadir productos a la FacturaVenta usando DetalleVenta
        for producto_id, cantidad, precio in zip(productos_ids, cantidades, precios):
            DetalleVenta.objects.create(
                factura=factura_venta,
                producto_id=producto_id,
                cantidad=cantidad,
                precio_venta=precio
            )
        
       

        # Redirigir a una página de éxito o la URL deseada
        return redirect('detalle_ventas')

    # Si no es POST, redirigir al formulario de creación de venta
    return redirect('detalle_ventas')