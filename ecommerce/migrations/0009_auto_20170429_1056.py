# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-29 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_auto_20170429_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='bus',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='mrt',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
