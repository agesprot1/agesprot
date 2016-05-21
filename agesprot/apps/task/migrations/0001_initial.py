# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-21 05:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tarea', models.CharField(max_length=45)),
                ('descripcion_tarea', models.CharField(max_length=100)),
                ('fecha_creacion', models.DateField(auto_now=True)),
                ('fecha_entrega', models.DateField()),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Tipo_estado')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_prioridad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_prioridad', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='tarea',
            name='prioridad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.Tipo_prioridad'),
        ),
    ]
