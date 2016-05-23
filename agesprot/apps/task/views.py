from agesprot.apps.project.models import Proyecto
from django.shortcuts import render

var_dir_template = 'task/'

def all_task_project(request, project):
	project = Proyecto.objects.get(pk = project)
	return render(request, var_dir_template+'list_task.html', {'project': project, 'title': 'Tareas del proyecto '+project.nombre_proyecto})