# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-17 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0009_user_celphone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='date',
            field=models.DateField(),
        ),
    ]