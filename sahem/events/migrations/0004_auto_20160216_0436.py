# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 04:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20160216_0332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]