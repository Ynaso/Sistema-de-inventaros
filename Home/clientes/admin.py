from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'direccion')
    search_fields = ('nombre', 'apellidos')
