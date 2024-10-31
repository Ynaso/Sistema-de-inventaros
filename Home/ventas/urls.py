from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.crear_venta, name="crear_venta"),
]