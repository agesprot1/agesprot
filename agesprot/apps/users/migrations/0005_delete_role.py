# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 21:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160516_1811'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Role',
        ),
    ]