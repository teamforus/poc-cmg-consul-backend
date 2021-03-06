# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0003_organisationrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationrequest',
            name='auth_token',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='organisationrequest',
            name='unique_key',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
