# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-10 00:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160310_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_images/%Y/%m/%d'),
        ),
    ]
