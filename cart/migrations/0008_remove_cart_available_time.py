# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-11 07:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_auto_20170511_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='available_time',
        ),
    ]
