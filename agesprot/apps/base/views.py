# -*- encoding: utf-8 -*-
from agesprot.apps.audit.register_activity import register_activity_profile_user
from django.contrib.auth.decorators import permission_required
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
import json

var_dir_template = 'home/'

class ListRolesProjectView(ListView):
	template_name = var_dir_template+'list_roles_project.html'
	model = Tipo_role

	def get_context_data(self, **kwargs):
		context = super(ListRolesProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Lista de Roles de projectos'
		return context

class ListPrioridadProjectView(ListView):
	template_name = var_dir_template+'list_prioridad_project.html'
	model = Tipo_prioridad

	def get_context_data(self, **kwargs):
		context = super(ListPrioridadProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Lista de Prioridades de projectos'
		return context

@permission_required('is_staff')
def form_role(request, role_pk):
	response = {}
	try:
		role = Tipo_role.objects.get(pk = role_pk)
		action = 'actualizado'
	except Tipo_role.DoesNotExist:
		role = role_pk
		action = 'creado'
	if request.method == 'POST':
		form = RoleProjectForm(request.POST, instance = role)
		if form.is_valid():
			project_response = form.save()
			response['type'] = 'success'
			response['pk'] = project_response.pk
			response['nombre_role'] = project_response.nombre_role
			response['msg'] = 'Operación exitosa'
			nombre_role = role.nombre_role if action != 'creado' else project_response.nombre_role
			register_activity_profile_user(request.user, 'Rol '+nombre_role+' '+action)
		else:
			response['type'] = 'error'
			response['msg'] = 'Ha ocurrido un error'
		return HttpResponse(json.dumps(response), "application/json")
	else:
		form = RoleProjectForm(instance = role)
	return render(request, var_dir_template+'form_role.html', {'forms': form, 'role': role_pk, 'title': 'Roles de proyectos'})

@permission_required('is_staff')
def delete_role(request, role_pk):
	response = {}
	role = Tipo_role.objects.get(pk = role_pk)
	register_activity_profile_user(request.user, 'Rol '+role.nombre_role+' eliminado')
	role.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar el rol'
	return HttpResponse(json.dumps(response), "application/json")

@permission_required('is_staff')
def form_prioridad(request, prioridad_pk):
	response = {}
	try:
		prioridad = Tipo_prioridad.objects.get(pk = prioridad_pk)
		action = 'actualizado'
	except Tipo_prioridad.DoesNotExist:
		prioridad = prioridad_pk
		action = 'creado'
	if request.method == 'POST':
		form = PrioridadProjectForm(request.POST, instance = prioridad)
		if form.is_valid():
			project_response = form.save()
			response['type'] = 'success'
			response['pk'] = project_response.pk
			response['color'] = project_response.color_prioridad
			response['nombre_prioridad'] = project_response.nombre_prioridad
			response['msg'] = 'Operación exitosa'
			nombre_prioridad = prioridad.nombre_prioridad if action != 'creado' else project_response.nombre_prioridad
			register_activity_profile_user(request.user, 'Prioridad '+nombre_prioridad+' '+action)
		else:
			response['type'] = 'error'
			response['msg'] = 'Ha ocurrido un error'
		return HttpResponse(json.dumps(response), "application/json")
	else:
		form = PrioridadProjectForm(instance = prioridad)
	return render(request, var_dir_template+'form_prioridad.html', {'forms': form, 'prioridad': prioridad_pk, 'title': 'prioridades de proyectos'})

@permission_required('is_staff')
def delete_prioridad(request, prioridad_pk):
	response = {}
	prioridad = Tipo_prioridad.objects.get(pk = prioridad_pk)
	register_activity_profile_user(request.user, 'Priodidad '+prioridad.nombre_prioridad+' eliminado')
	prioridad.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar la prioridad'
	return HttpResponse(json.dumps(response), "application/json")