# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-10 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='participants_number',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='participants_number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
