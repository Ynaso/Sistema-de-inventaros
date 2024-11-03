# urls.py
from django.urls import path
from .views import crear_compra, procesar_compra, detalle_compra

urlpatterns = [
    # Other URL patterns
    path('', crear_compra, name='crear_compra'),  # URL for the purchase form
    path('procesar_compra/', procesar_compra, name='procesar_compra'),  # URL for processing the purchase
    path('detalle_compras/', detalle_compra, name='detalle_compras')
]
