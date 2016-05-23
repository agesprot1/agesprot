from django.contrib.auth.models import User
from .models import *

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