# -*- encoding: utf-8 -*-
from agesprot.apps.base.models import Tipo_estado, Tipo_prioridad
from agesprot.apps.project.models import Roles_project
from django.forms import *
from django import forms
from .models import *

class ActivitieForm(forms.ModelForm):
	class Meta:
		model = Actividad
		fields = '__all__'
		exclude = ['proyecto', 'estado']
		widgets = {
			'nombre_actividad': TextInput(attrs = {'class': 'form-control', 'maxlength': '45', 'required': True}),
			'descripcion_actividad': Textarea(attrs = {'rows': 5, 'class': 'form-control', 'maxlength': '300', 'required': True}),
			'fecha_entrega': TextInput(attrs = {'class': 'form-control date', 'required': True}),
		}
		labels = {
			'nombre_proyecto': 'Nombre de la actividad',
			'descripcion_actividad': 'Descripción',
			'fecha_entrega': 'Fecha de entrega',
		}

	def clean_prioridad(self):
		return Tipo_prioridad.objects.get(pk = self.cleaned_data.get('prioridad'))

	def __init__(self, *args, **kwargs):
		super(ActivitieForm, self).__init__(*args, **kwargs)
		self.fields['prioridad'] = forms.ChoiceField(label = "Prioridad", choices = [('', 'Seleccione un prioridad')]+[(x.pk, x.nombre_prioridad) for x in Tipo_prioridad.objects.all()], widget = forms.Select(attrs = {'class': 'form-control chosen', 'required': True}))

class UserRoleForm(forms.ModelForm):
	class Meta:
		model = Actividad_role
		fields = '__all__'
		exclude = ['actividad']
		labels = {
			'role': 'Usuario'
		}

	def clean_role(self):
		return Roles_project.objects.get(pk = self.cleaned_data.get('role'))

	def __init__(self, *args, **kwargs):
		proyecto = kwargs.pop('proyecto', None)
		user_list = [x.role.pk for x in Actividad_role.objects.filter(actividad = kwargs.pop('actividad', None))]
		super(UserRoleForm, self).__init__(*args, **kwargs)
		self.fields['role'] = forms.ChoiceField(label = "Usuario", choices = [('', 'Seleccione un usuario')]+[(x.pk, x.user.first_name+" "+x.user.last_name+" - "+x.user.email) for x in Roles_project.objects.filter(proyecto = proyecto).exclude(pk__in = user_list)], widget = forms.Select(attrs = {'class': 'form-control chosen', 'required': True}))