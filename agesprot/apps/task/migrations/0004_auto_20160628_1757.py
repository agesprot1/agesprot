# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-28 22:57
from __future__ import unicode_literals

import agesprot.apps.task.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_remove_documento_tipo_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='documento',
            field=models.FileField(upload_to=agesprot.apps.task.models.get_path),
        ),
    ]