# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 22:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0018_auto_20160308_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
