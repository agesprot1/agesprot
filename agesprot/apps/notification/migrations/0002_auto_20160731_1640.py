# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-31 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationuser',
            name='titulo_notificacion',
            field=models.CharField(max_length=100),
        ),
    ]