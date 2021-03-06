# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-29 11:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0044_ordering_voucher'),
        ('index', '0004_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexVendorRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(unique=True)),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.IndexPage')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Vendor')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
