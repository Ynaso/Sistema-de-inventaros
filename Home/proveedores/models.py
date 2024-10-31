from django.db import models

class TipoCompra(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_proveedor = models.ForeignKey(TipoCompra, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)
    numero_ruc = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre
