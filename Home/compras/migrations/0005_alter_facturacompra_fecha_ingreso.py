# Generated by Django 4.1.3 on 2024-11-03 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0004_tipocompra_facturacompra_tipo_compra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturacompra',
            name='fecha_ingreso',
            field=models.DateField(auto_now_add=True),
        ),
    ]
