# -*- encoding: utf-8 -*-
from django.forms import *
from django import forms
from .models import *

class RoleProjectForm(forms.ModelForm):
	class Meta:
		model = Tipo_role
		fields = '__all__'
		widgets = {
			'nombre_role': TextInput(attrs = {'class': 'form-control', 'maxlength': '45'})
		}
		labels = {
			'nombre_role': 'Nombre del role'
		}

class PrioridadProjectForm(forms.ModelForm):
	class Meta:
		model = Tipo_prioridad
		fields = '__all__'
		widgets = {
			'nombre_prioridad': TextInput(attrs = {'class': 'form-control', 'maxlength': '45', 'required': True}),
			'color_prioridad': TextInput(attrs = {'class': 'form-control', 'required': True})
		}
		labels = {
			'color_prioridad': 'Color'
		}