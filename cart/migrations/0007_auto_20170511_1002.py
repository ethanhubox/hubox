# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-11 02:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_cart_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
