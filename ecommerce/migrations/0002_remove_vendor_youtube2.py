# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-25 18:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='youtube2',
        ),
    ]
