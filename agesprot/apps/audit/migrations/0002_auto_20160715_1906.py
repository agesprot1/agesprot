# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-16 00:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AuditoryProfileUser',
            new_name='AuditProfileUser',
        ),
    ]
