# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 01:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_auto_20160527_2049'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tarea_integrantes',
            new_name='Tarea_integrante',
        ),
    ]
