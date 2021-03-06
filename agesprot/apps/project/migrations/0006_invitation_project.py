# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-23 21:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_delete_tipo_documento'),
        ('project', '0005_auto_20160812_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Proyecto')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Tipo_role')),
            ],
        ),
    ]
