# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-28 09:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0005_auto_20180926_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationrequest',
            name='is_subscribe',
            field=models.BooleanField(default=False),
        ),
    ]
