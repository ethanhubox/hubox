# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-02 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0022_auto_20170501_1801'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursemedia',
            options={'ordering': ['course', 'order']},
        ),
        migrations.AlterModelOptions(
            name='vendormedia',
            options={'ordering': ['vendor', 'position', 'order']},
        ),
        migrations.AddField(
            model_name='coursemedia',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendormedia',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
