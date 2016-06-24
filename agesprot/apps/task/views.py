from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from agesprot.apps.activity.models import Actividad
from agesprot.apps.project.models import Proyecto
from agesprot.apps.base.models import Tipo_estado
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
import datetime
import json

var_dir_template = 'task/'

class NewTaskActivityView(SuccessMessageMixin, CreateView):
	template_name = var_dir_template+'form_task.html'
	success_message = 'Tarea creada con exito.'
	form_class = TareaForm

	def get_context_data(self, **kwargs):
		context = super(NewTaskActivityView, self).get_context_data(**kwargs)
		activity = Actividad.objects.get(pk = self.kwargs['pk_activity'])
		context['title'] = 'Crear una nueva tarea'
		context['activity'] = activity
		context['url'] = '/project/'+self.kwargs['pk']+'/'+self.kwargs['tag_url']+'/activities/'+self.kwargs['pk_activity']+'/task/add-task-activity/'
		return context

	def form_valid(self, form):
		form.instance.actividad = Actividad.objects.get(pk = self.kwargs['pk_activity'])
		form.instance.estado = Tipo_estado.objects.get(nombre_estado = 'Proceso')
		form.instance.usuario = self.request.user
		return super(NewTaskActivityView, self).form_valid(form)

	def get_success_url(self):
		return reverse('detail_activities', args = (self.kwargs['pk'], self.kwargs['tag_url'], self.kwargs['pk_activity']))

class UpdateTaskActivityView(SuccessMessageMixin, UpdateView):
	model = Tarea
	template_name = var_dir_template+'form_task.html'
	success_message = 'Tarea actualizada con exito.'
	form_class = TareaForm

	def get_object(self):
		return Tarea.objects.get(pk = self.kwargs['pk_task'])

	def get_context_data(self, **kwargs):
		context = super(UpdateTaskActivityView, self).get_context_data(**kwargs)
		activity = Actividad.objects.get(pk = self.kwargs['pk_activity'])
		context['title'] = 'Editar tarea'
		context['activity'] = activity
		context['url'] = '/project/'+self.kwargs['pk']+'/'+self.kwargs['tag_url']+'/activities/'+self.kwargs['pk_activity']+'/task/'+self.kwargs['pk_task']+'/update-task/'
		return context

	def form_valid(self, form):
		estado = Tipo_estado.objects.all()
		form.instance.actividad = Actividad.objects.get(pk = self.kwargs['pk_activity'])
		form.instance.estado = estado.get(nombre_estado = 'Proceso') if form.cleaned_data['fecha_entrega'] >= datetime.datetime.now().date() else estado.get(nombre_estado = 'Terminado')
		return super(UpdateTaskActivityView, self).form_valid(form)

	def get_success_url(self):
		return reverse('detail_activities', args = (self.kwargs['pk'], self.kwargs['tag_url'], self.kwargs['pk_activity']))

class DetailTaskView(DetailView):
	template_name = var_dir_template+'detail_task.html'
	model = Tarea

	def get_context_data(self, **kwargs):
		context = super(DetailTaskView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['project'] = data_project
		context['title'] = 'Detalle de la tarea '
		return context

	def get_object(self):
		return Tarea.objects.get(pk = self.kwargs['pk_task'])

class NewTaskCommentView(SuccessMessageMixin, CreateView):
	template_name = var_dir_template+'form_task_comment.html'
	success_message = 'Tarea creada con exito.'
	form_class = ComentarioTareaForm

	def get_context_data(self, **kwargs):
		context = super(NewTaskCommentView, self).get_context_data(**kwargs)
		context['project'] = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['object'] = Tarea.objects.get(pk = self.kwargs['pk_task'])
		return context

	def form_valid(self, form):
		form.instance.tarea = Tarea.objects.get(pk = self.kwargs['pk_task'])
		form.instance.usuario = self.request.user
		return super(NewTaskCommentView, self).form_valid(form)

	def get_success_url(self):
		return reverse('detail_task', args = (self.kwargs['pk'], self.kwargs['tag_url'], self.kwargs['pk_activity'], self.kwargs['pk_task']))

@login_required
def delete_task(request, pk, tag_url, pk_activity, pk_task):
	response = {}
	tarea = Tarea.objects.get(pk = pk_task)
	tarea.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar la tarea'
	return HttpResponse(json.dumps(response), "application/json")

@login_required
def delete_comment(request, pk, tag_url, pk_activity, pk_task, pk_comment):
	response = {}
	comment = Comentario_tarea.objects.get(pk = pk_comment)
	comment.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar el comentario'
	return HttpResponse(json.dumps(response), "application/json")