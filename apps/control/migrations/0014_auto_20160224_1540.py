# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-24 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0013_auto_20160224_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='height',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
