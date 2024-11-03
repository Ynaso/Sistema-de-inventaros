# Generated by Django 4.1.3 on 2024-11-02 23:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='fecha_registro',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='cliente',
            name='ruc',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]