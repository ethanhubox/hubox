# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-28 02:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseorder', '0003_auto_20170526_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorder',
            name='voucher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Voucher'),
        ),
    ]