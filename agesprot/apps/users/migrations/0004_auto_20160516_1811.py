# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 23:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160515_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='foto',
            field=models.ImageField(default='img/none.png', upload_to='img/users/'),
        ),
    ]
