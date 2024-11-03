from django.db import models

class TipoProveedor(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_proveedor = models.ForeignKey(TipoProveedor, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    numero_ruc = models.CharField(max_length=15)
    telefono = models.CharField(max_length=15)  # New field for phone number
    direccion = models.CharField(max_length=255)  # New field for address

    def __str__(self):
        return self.nombre
