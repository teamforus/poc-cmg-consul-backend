# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0004_auto_20180926_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationrequest',
            name='data',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='organisationrequest',
            name='auth_token',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
