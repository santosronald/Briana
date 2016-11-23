# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-08 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0023_auto_20160405_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='messages', verbose_name='imagen'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(verbose_name='Texto'),
        ),
        migrations.AlterField(
            model_name='stimulation',
            name='month',
            field=models.CharField(choices=[('1', '1 mes'), ('2', '2 meses'), ('3', '3 meses'), ('4', '4 meses'), ('5', '5 meses'), ('6', '6 meses'), ('7', '7 meses'), ('8', '8 meses'), ('9', '9 meses'), ('10', '10 meses'), ('11', '11 meses'), ('12', '12 meses'), ('14', '14 meses'), ('16', '16 meses'), ('18', '18 meses'), ('20', '20 meses'), ('22', '22 meses'), ('24', '24 meses'), ('30', '30 meses'), ('36', '36 meses'), ('48', '48 meses')], max_length=2, verbose_name='Mes'),
        ),
        migrations.AlterField(
            model_name='stimulation',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Nombre'),
        ),
    ]
