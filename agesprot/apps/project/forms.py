# -*- encoding: utf-8 -*-
from django.forms import *
from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Proyecto
		fields = '__all__'
		exclude = ('estado', 'user')
		widgets = {
			'nombre_proyecto': TextInput(attrs = {'class': 'form-control', 'maxlength': '45', 'required': True}),
			'descripcion': TextInput(attrs = {'class': 'form-control', 'maxlength': '200', 'required': True}),
			'fecha_inicio': TextInput(attrs = {'class': 'form-control date_init', 'required': True}),
			'fecha_final': TextInput(attrs = {'class': 'form-control date_end', 'required': True}),
		}
		labels = {
			'nombre_proyecto': 'Nombre del proyecto',
			'descripcion': 'Descripcion del proyecto',
			'fecha_inicio': 'Fecha de inicio',
			'fecha_final': 'Fecha de finalización',
		}

class RoleProjectForm(forms.ModelForm):
	class Meta:
		model = Project_role
		fields = '__all__'
		widgets = {
			'nombre_role': TextInput(attrs = {'class': 'form-control', 'maxlength': '45'})
		}
		labels = {
			'nombre_role': 'Nombre del role'
		}