# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-04 22:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinations', '0005_vaccine_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vaccine',
            options={'ordering': ('order',), 'verbose_name': 'Vacuna', 'verbose_name_plural': 'Vacunas'},
        ),
    ]