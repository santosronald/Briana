# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-10 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0007_auto_20160210_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]