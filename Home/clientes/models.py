from django.db import models
import datetime

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    ruc = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_registro = models.DateField(default=datetime.date.today)  # Valor predeterminado explícito

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
