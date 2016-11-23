# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-03 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0016_auto_20160226_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='messages')),
                ('text', models.TextField()),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
    ]