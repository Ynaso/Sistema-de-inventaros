from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import FacturaCompra, DetalleCompra
from productos.models import Producto
from proveedores.models import Proveedor
from django.db import transaction
from kardex.models import Kardex
from .models import TipoCompra
from django.db.models import Subquery, OuterRef

def crear_compra(request):
    """ Renderiza el formulario para crear una nueva compra. """
    proveedores = Proveedor.objects.all()
    kardex_subquery = Kardex.objects.filter(
        producto=OuterRef('pk')
    ).order_by('-fecha_movimiento')

    # Anotamos productos con su último saldo, costo unitario y precio de venta
    productos = Producto.objects.annotate(
        stock=Subquery(kardex_subquery.values('saldo')[:1]),
        costo_unitario=Subquery(kardex_subquery.values('costo_unitario')[:1]),
        precio_venta=Subquery(kardex_subquery.values('precio_venta')[:1])
    )

    tipos_compra = TipoCompra.objects.all()

    return render(request, "compras/factura_compra.html", {
        'productos': productos,
        'proveedores': proveedores,
        'tipos_compra': tipos_compra
    })

def detalle_compra(request):
    """ Renderiza la vista de detalle para las compras. """
    detalles = DetalleCompra.objects.select_related('producto', 'factura').all()
    return render(request, "Compras/detalle_compras.html", {
        'detalles': detalles
    })

@transaction.atomic
def procesar_compra(request):
    """ Procesa la sumisión de una compra. """
    if request.method == "POST":
        
        print(request.POST)
        proveedor_id = request.POST.get('proveedor')
        responsable = "Yonis Alvarez"
        
        # Usa el sufijo [] para recibir los datos como listas
        productos_ids = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        costos = request.POST.getlist('costo')
        tipo_compra = request.POST.get('tipo_compra')

        print(productos_ids)
        print(cantidades)
        print(precios)
        print(costos)
        print(tipo_compra)

        # Validación de datos
        factura_compra = FacturaCompra.objects.create(
                proveedor_id=proveedor_id,
                responsable=responsable,
                tipo_compra_id=tipo_compra,
        )

        
        print(f"Factura creada: {factura_compra.id}")

        # Agregar productos a la factura a través de DetalleCompra
        for producto_id, cantidad, precio, costo in zip(productos_ids, cantidades, precios, costos):
            DetalleCompra.objects.create(
                factura=factura_compra,
                producto_id=producto_id,
                cantidad=int(cantidad),  # Asegúrate de convertir a int si necesario
                precio_unitario=float(precio),  # Asegúrate de convertir a float
                costo_unitario=float(costo)  # Asegúrate de convertir a float
        )
        
        # Redirige a la vista de detalle de compras tras el procesamiento
        return redirect('detalle_ventas')

    # Redirige al formulario si la solicitud no es POST
    return redirect('detalle_ventas')
