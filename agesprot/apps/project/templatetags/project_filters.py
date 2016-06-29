# -*- encoding: utf-8 -*-
from django import template
from agesprot.apps.project.models import *
from agesprot.apps.activity.models import *
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