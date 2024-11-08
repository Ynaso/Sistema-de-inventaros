# Generated by Django 5.1.2 on 2024-10-29 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=50)),
                ('numero_ruc', models.CharField(max_length=15)),
                ('tipo_proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proveedores.tipocompra')),
            ],
        ),
    ]
