from django.db import models

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)  # ID auto generado
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class EstadoProducto(models.Model):
    id = models.AutoField(primary_key=True)  # ID auto generado
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.estado

class Producto(models.Model):
    id = models.AutoField(primary_key=True)  # ID auto generado
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoProducto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
