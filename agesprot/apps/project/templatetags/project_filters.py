# -*- encoding: utf-8 -*-
from django import template
from django.db.models import Count
from agesprot.apps.project.models import *
from agesprot.apps.activity.models import *
from agesprot.apps.base.models import Tipo_estado
register = template.Library()

def verify_user_project(project, user):
	try:
		project = Proyecto.objects.get(pk = project).roles_project_set.get(user = user).user
		return True
	except:
		return False

def verify_user_project_administrator(project, user):
	try:
		return True if Proyecto.objects.get(pk = project).roles_project_set.get(user = user).role.nombre_role == "Administrador" else False
	except:
		False

def regla_tres(a, b):
	return int((a*100)/b)

@register.filter
def verify_admin_project(user, project):
	try:
		return True if Proyecto.objects.get(pk = project).roles_project_set.get(user = user).role.nombre_role == "Administrador" else False
	except:
		False

@register.filter
def verify_user_activity(user, actividad):
	actividad = Actividad.objects.get(pk = actividad)
	role = Roles_project.objects.get(user = user, proyecto = actividad.proyecto.pk)
	try:
		return True if Actividad_role.objects.get(role = role, actividad = actividad) else False
	except:
		False

@register.filter
def count_project(type_count, object_data):
	project = Proyecto.objects.all()
	state = Tipo_estado.objects.all()
	state_active = state.get(nombre_estado = 'Activo')
	state_terminate = state.get(nombre_estado = 'Terminado')
	count_tot = 0
	if type_count == 'all_me':
		count_tot = project.filter(user = object_data).count()
	elif type_count == 'all':
		count_tot = project.filter(roles_project__user = object_data).count()
	elif type_count == 'all_end':
		count_tot = project.filter(estado = state_terminate, roles_project__user = object_data).count()
	elif type_count == 'all_pro':
		count_tot = project.filter(estado = state_active, roles_project__user = object_data).count()
	elif type_count == 'activities':
		count_tot = project.filter(actividad__proyecto = object_data).count()
	elif type_count == 'tasks':
		for count_activity in Actividad.objects.filter(proyecto = object_data):
			count_tot = count_tot + count_activity.tarea_set.all().count()
	elif type_count == 'users':
		count_tot = Roles_project.objects.filter(proyecto = object_data).count()
	elif type_count == 'progress':
		activity_tot = Actividad.objects.filter(proyecto = object_data)
		activity_terminate = activity_tot.filter(estado = state_terminate).count()
		count_tot = regla_tres(activity_terminate, activity_tot.count()) if activity_tot.count() > 0 else 0
	return count_tot

@register.filter
def sum_activity(num, value):
	return value + num