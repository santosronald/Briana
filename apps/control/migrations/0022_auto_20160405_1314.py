# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-05 18:14
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0021_auto_20160405_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dni',
            field=models.CharField(blank=True, max_length=8, validators=[django.core.validators.RegexValidator(message='El dni debe ser de 8 números', regex='^.{8}$')]),
        ),
    ]
