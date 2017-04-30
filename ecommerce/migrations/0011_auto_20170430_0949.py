# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-30 01:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_auto_20170430_0946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='availabletime',
            options={'ordering': ['course', 'date', 'start_time']},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['vendor']},
        ),
        migrations.AlterModelOptions(
            name='coursemedia',
            options={'ordering': ['course']},
        ),
        migrations.AlterModelOptions(
            name='indexrole',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='indexvendor',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='vendormedia',
            options={'ordering': ['vendor', 'position']},
        ),
    ]
