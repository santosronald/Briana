# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-08 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='address',
            field=models.CharField(blank=True, max_length=200, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='center',
            name='center_type',
            field=models.CharField(choices=[('HOSPITAL', 'Hospital'), ('CLINIC', 'Clinica'), ('POSTA', 'Posta'), ('OTHER', 'Otro')], max_length=10, verbose_name='Tipo de Centro'),
        ),
        migrations.AlterField(
            model_name='center',
            name='description',
            field=models.TextField(verbose_name='descripción'),
        ),
        migrations.AlterField(
            model_name='center',
            name='monday_to_friday',
            field=models.CharField(max_length=25, verbose_name='Lunes a Viernes'),
        ),
        migrations.AlterField(
            model_name='center',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='center',
            name='saturday_sunday_holiday',
            field=models.CharField(max_length=25, verbose_name='Fines de semana y feriados'),
        ),
    ]
