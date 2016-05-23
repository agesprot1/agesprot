# -*- encoding: utf-8 -*-
from agesprot.apps.base.models import Tipo_role
from django.contrib.auth.models import User
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

	def save(self):
		nombre_proyecto = self.cleaned_data.get('nombre_proyecto')
		descripcion = self.cleaned_data.get('descripcion')
		fecha_inicio = self.cleaned_data.get('fecha_inicio')
		fecha_final = self.cleaned_data.get('fecha_final')
		user = User.objects.get(pk = self.instance.user.pk)
		proyecto = Proyecto(nombre_proyecto = nombre_proyecto, descripcion = descripcion, fecha_inicio = fecha_inicio, fecha_final = fecha_final, user = user)
		proyecto.save()
		role = Tipo_role.objects.get(nombre_role = "Administrador")
		project_role = Roles_project(user = user, proyecto = proyecto, role = role)
		project_role.save()
		return proyecto

class AddUserProjectForm(forms.ModelForm):
	class Meta:
		model = Roles_project
		fields = '__all__'
		exclude = ['proyecto']

	def clean_user(self):
		return User.objects.get(pk = self.cleaned_data.get('user'))

	def clean_role(self):
		return Tipo_role.objects.get(pk = self.cleaned_data.get('role'))

	def __init__(self, *args, **kwargs):
		project = kwargs.pop('instance', None)
		user_list = [x.user.pk for x in Roles_project.objects.filter(proyecto = project.pk)]
		super(AddUserProjectForm, self).__init__(*args, **kwargs)
		self.fields['user'] = forms.ChoiceField(label = "Usuario", choices = [('', 'Seleccione un usuario')]+[(x.pk, x.first_name+" "+x.last_name) for x in User.objects.exclude(pk__in = user_list).distinct()], widget = forms.Select(attrs = {'class': 'form-control', 'required': True}))
		self.fields['role'] = forms.ChoiceField(label = "Rol", choices = [('', 'Seleccione un rol')]+[(x.pk, x.nombre_role) for x in Tipo_role.objects.all()], widget = forms.Select(attrs = {'class': 'form-control', 'required': True}))