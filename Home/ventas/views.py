from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import FacturaVenta, DetalleVenta, TipoVenta
from productos.models import Producto
from clientes.models import Cliente
from kardex.models import Kardex
from django.db.models import Sum, F, OuterRef, Subquery

from django.db import transaction
from django.utils.timezone import now

@transaction.atomic  # Garantiza que toda la transacción se haga correctamente o se revierta
def crear_venta(request):
   

    kardex_subquery = Kardex.objects.filter(
        producto=OuterRef('pk')
    ).order_by('-fecha_movimiento')

    # Main query to annotate Productos with stock, costo_unitario, and precio_venta
    productos = Producto.objects.annotate(
        stock=Sum('kardex__cantidad'),
        costo_unitario=Subquery(kardex_subquery.values('costo_unitario')[:1]),
        precio_venta=Subquery(kardex_subquery.values('precio_venta')[:1])
    )
    clientes = Cliente.objects.all()  # Obtener todos los clientes
    tipos_venta = TipoVenta.objects.all()  # Obtener los tipos de venta

    if request.method == "POST":
        # Recibir los datos del formulario
        cliente_id = request.POST.get('cliente')
        tipo_venta_id = request.POST.get('tipo_venta')
        productos_ids = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')

        if not (cliente_id and productos_ids and cantidades):
            return HttpResponse("Todos los campos son requeridos", status=400)

        # Crear la factura
        factura = FacturaVenta.objects.create(
            numero_factura=f"F-{now().strftime('%Y%m%d%H%M%S')}",  # Generar número de factura único
            cliente_id=cliente_id,
            fecha_salida=now().date(),
            tipo_venta_id=tipo_venta_id
        )

        # Crear los detalles de la venta
        for i, producto_id in enumerate(productos_ids):
            DetalleVenta.objects.create(
                factura=factura,
                producto_id=producto_id,
                cantidad=int(cantidades[i]),
                precio_venta=float(precios[i])
            )

        return redirect(reverse('factura_detalle', args=[factura.id]))  # Redirige a una vista de detalle

    # Enviar los datos al template
    context = {
        'productos': productos,
        'clientes': clientes,
        'tipos_venta': tipos_venta
    }
    return render(request, 'Ventas/factura_venta.html', context)
