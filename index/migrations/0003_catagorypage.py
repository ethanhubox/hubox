# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-15 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import index.models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_memberterms_privacypolicy'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatagoryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('banner', models.FileField(upload_to=index.models.catagory_page_media)),
            ],
        ),
    ]
