# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-10 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0005_child_relationship'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='control',
            name='age',
        ),
        migrations.AddField(
            model_name='control',
            name='date',
            field=models.DateField(auto_now=True, default='1991-12-12'),
            preserve_default=False,
        ),
    ]
