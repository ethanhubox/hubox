# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-18 12:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0043_voucher'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordering',
            name='voucher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Voucher'),
        ),
    ]
