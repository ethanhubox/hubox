# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-01 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0020_auto_20170501_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='subscribe',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
