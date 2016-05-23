# -*- encoding: utf-8 -*-
from django import template
from agesprot.apps.project.models import Proyecto
register = template.Library()

@register.filter
def verify_admin_project(user, project):
	return True if Proyecto.objects.get(pk = project).roles_project_set.get(user = user).role.nombre_role == "Administrador" else False