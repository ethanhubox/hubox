# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-30 01:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0015_auto_20170430_0955'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='availabletime',
            options={'ordering': ['course', 'date', 'start_time']},
        ),
    ]
