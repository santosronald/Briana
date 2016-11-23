# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-26 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinations', '0007_auto_20160218_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccine',
            name='month',
        ),
        migrations.AlterField(
            model_name='vaccine',
            name='after_months',
            field=models.PositiveSmallIntegerField(default=2),
            preserve_default=False,
        ),
    ]
