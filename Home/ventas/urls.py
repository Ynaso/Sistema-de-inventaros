from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.formulario_venta, name="crear_venta"),
    path('procesar_venta/', views.procesar_venta, name="procesar_venta"),
    path('detalle_ventas/', views.detalle_ventas, name='detalle_ventas'),
    
]