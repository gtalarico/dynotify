# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-03 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynotify', '0003_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
