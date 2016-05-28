from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, CreateView
from agesprot.apps.project.models import Proyecto
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .models import *
from .forms import *

var_dir_template = 'task/'

class ListTaskProjectView(DetailView):
	template_name = var_dir_template+'list_task.html'
	model = Proyecto

	def get_context_data(self, **kwargs):
		context = super(ListTaskProjectView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Tareas del proyecto '+data_project.nombre_proyecto
		context['project'] = data_project
		return context

class NewTaskView(SuccessMessageMixin, CreateView):
	template_name = var_dir_template+'form_task.html'
	success_message = 'Tarea creada con exito.'
	form_class = Tarea_form

	def get_context_data(self, **kwargs):
		self.pk = self.kwargs['pk']
		context = super(NewTaskView, self).get_context_data(**kwargs)
		context['title'] = 'Crear una nueva tarea'
		context['project_pk'] = self.pk
		return context

	def form_valid(self, form):
		form.instance.proyecto = Proyecto.objects.get(pk = self.kwargs['pk'])
		form.save()
		return super(NewTaskView, self).form_valid(form)

	def get_success_url(self):
		return reverse('all_task_project', kwargs = {'pk': self.kwargs['pk']})

def list_integrant_task(request, *args, **kwargs):
	task_integrant = Tarea.objects.get(pk = kwargs['task'])
	return render(request, var_dir_template+'list_task_integrant.html', {'task_integrant': task_integrant, 'title': 'Integrantes de la tarea '+task_integrant.nombre_tarea})