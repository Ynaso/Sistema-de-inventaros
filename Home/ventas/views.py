from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from .models import FacturaVenta, DetalleVenta, TipoVenta
from productos.models import Producto
from clientes.models import Cliente
from kardex.models import Kardex
from django.db.models import Sum, OuterRef, Subquery
from django.db import transaction
from django.utils import timezone

def formulario_venta(request):
    # Cargar datos necesarios para el formulario
    kardex_subquery = Kardex.objects.filter(
        producto=OuterRef('pk')
    ).order_by('-fecha_movimiento')

    productos = Producto.objects.annotate(
        stock=Sum('kardex__cantidad'),
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

@transaction.atomic
def procesar_venta(request):
    if request.method == "POST":
        cliente_id = request.POST.get('cliente')
        tipo_venta_id = request.POST.get('tipo_venta')
        productos_ids = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')

        # Validar que los datos necesarios están presentes
        if not (cliente_id and productos_ids and cantidades and precios):
            return HttpResponseBadRequest("Incomplete form submission")

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
        return redirect('procesar_venta')

    # Si no es POST, redirigir al formulario de creación de venta
    return redirect('Ventas/factura_venta.html')
