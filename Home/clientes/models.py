from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
