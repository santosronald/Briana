# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 00:25
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0008_auto_20160210_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='celphone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128),
        ),
    ]
