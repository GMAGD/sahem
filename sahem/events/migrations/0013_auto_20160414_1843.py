# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20160314_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='comments',
            field=models.ManyToManyField(null=True, to='events.Comment'),
        ),
    ]
