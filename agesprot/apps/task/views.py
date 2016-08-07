from django.views.generic import DetailView, CreateView, UpdateView
from agesprot.apps.notification.utils import register_notification
from agesprot.apps.project.templatetags.project_filters import *
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from agesprot.apps.activity.models import Actividad
from agesprot.apps.project.models import Proyecto
from agesprot.apps.base.models import Tipo_estado
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str
from agesprot.apps.audit.utils import *
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
		actividad = Actividad.objects.get(pk = self.kwargs['pk_activity'])
		form.instance.actividad = actividad
		form.instance.estado = Tipo_estado.objects.get(nombre_estado = 'Proceso')
		form.instance.usuario = self.request.user
		form_data = form.save()
		register_activity_profile_user(self.request.user, 'Tarea '+form_data.nombre_tarea+' creada en la actividad '+actividad.nombre_actividad+' del proyecto '+actividad.proyecto.nombre_proyecto)
		register_activity_project(self.request.user, actividad.proyecto, 'Tarea '+form_data.nombre_tarea+' creada en la actividad '+actividad.nombre_actividad+' del proyecto '+actividad.proyecto.nombre_proyecto)
		for users in actividad.actividad_role_set.all():
			register_notification(users.role.user, 'fa-tasks', 'La tarea <a href="/project/'+str(actividad.proyecto.pk)+'/'+actividad.proyecto.tag_url+'/activities/'+str(actividad.pk)+'/task/'+str(form_data.pk)+'/detail-task/">'+form_data.nombre_tarea+'</a> ha sido creada dentro de la actividad <a href="/project/'+str(actividad.proyecto.pk)+'/'+actividad.proyecto.tag_url+'/activities/'+str(actividad.pk)+'/detail-activity/">'+actividad.nombre_actividad+'</a> del proyecto <a href="/project/'+str(actividad.proyecto.pk)+'/'+actividad.proyecto.tag_url+'/">'+actividad.proyecto.nombre_proyecto+'</a>')
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
		actividad = Actividad.objects.get(pk = self.kwargs['pk_activity'])
		form.instance.actividad = actividad
		form.instance.estado = estado.get(nombre_estado = 'Proceso') if form.cleaned_data['fecha_entrega'] >= datetime.datetime.now().date() else estado.get(nombre_estado = 'Terminado')
		form_data = form.save()
		register_activity_profile_user(self.request.user, 'Tarea '+form_data.nombre_tarea+' actualizada en la actividad '+actividad.nombre_actividad+' del proyecto '+actividad.proyecto.nombre_proyecto)
		register_activity_project(self.request.user, actividad.proyecto, 'Tarea '+form_data.nombre_tarea+' actualizada en la actividad '+actividad.nombre_actividad+' del proyecto '+actividad.proyecto.nombre_proyecto)
		for users in actividad.actividad_role_set.all():
			register_notification(users.role.user, 'fa-tasks', 'La tarea <a href="/project/'+str(actividad.proyecto.pk)+'/'+actividad.proyecto.tag_url+'/activities/'+str(actividad.pk)+'/task/'+str(form_data.pk)+'/detail-task/">'+form_data.nombre_tarea+'</a> ha sido editada dentro de la actividad <a href="/project/'+str(actividad.proyecto.pk)+'/'+actividad.proyecto.tag_url+'/activities/'+str(actividad.pk)+'/detail-activity/">'+actividad.nombre_actividad+'</a> del proyecto <a href="/project/'+str(actividad.proyecto.pk)+'/'+actividad.proyecto.tag_url+'/">'+actividad.proyecto.nombre_proyecto+'</a>')
		return super(UpdateTaskActivityView, self).form_valid(form)

	def get_success_url(self):
		return reverse('detail_activities', args = (self.kwargs['pk'], self.kwargs['tag_url'], self.kwargs['pk_activity']))

class DetailTaskView(DetailView):
	template_name = var_dir_template+'detail_task.html'
	model = Tarea

	def get(self, request, **kwargs):
		self.object = self.get_object()
		verify = verify_user_project(self.object.actividad.proyecto.pk, self.request.user)
		context = self.get_context_data(object=self.object)
		detail_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return self.render_to_response(context) if verify is True else HttpResponseRedirect(reverse('RestrProject', kwargs = {'pk_project': detail_project.pk}))

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
		tarea = Tarea.objects.get(pk = self.kwargs['pk_task'])
		form.instance.tarea = tarea
		form.instance.usuario = self.request.user
		form_data = form.save()
		register_activity_profile_user(self.request.user, 'Comentario agregado en la tarea '+tarea.nombre_tarea+' de la actividad '+tarea.actividad.nombre_actividad+' del proyecto '+tarea.actividad.proyecto.nombre_proyecto)
		register_activity_project(self.request.user, tarea.actividad.proyecto, 'Comentario agregado en la tarea '+tarea.nombre_tarea+' de la actividad '+tarea.actividad.nombre_actividad+' del proyecto '+tarea.actividad.proyecto.nombre_proyecto)
		for users in tarea.actividad.actividad_role_set.all():
			register_notification(users.role.user, 'fa-comments', 'Hay un nuevo comentario en la tarea <a href="/project/'+str(tarea.actividad.proyecto.pk)+'/'+tarea.actividad.proyecto.tag_url+'/activities/'+str(tarea.actividad.pk)+'/task/'+str(tarea.pk)+'/detail-task/">'+tarea.nombre_tarea+'</a> de la actividad <a href="/project/'+str(tarea.actividad.proyecto.pk)+'/'+tarea.actividad.proyecto.tag_url+'/activities/'+str(tarea.actividad.pk)+'/detail-activity/">'+tarea.actividad.nombre_actividad+'</a> del proyecto <a href="/project/'+str(tarea.actividad.proyecto.pk)+'/'+tarea.actividad.proyecto.tag_url+'/">'+tarea.actividad.proyecto.nombre_proyecto+'</a>')
		return super(NewTaskCommentView, self).form_valid(form)

	def get_success_url(self):
		return reverse('detail_task', args = (self.kwargs['pk'], self.kwargs['tag_url'], self.kwargs['pk_activity'], self.kwargs['pk_task']))

class UploadFileView(SuccessMessageMixin, CreateView):
	template_name = var_dir_template+'form_task_document.html'
	success_message = 'Documento agregado con exito.'
	form_class = DocumentoTareaForm

	def get_context_data(self, **kwargs):
		context = super(UploadFileView, self).get_context_data(**kwargs)
		context['title'] = 'Nuevo documento'
		context['url'] = '/project/'+self.kwargs['pk']+'/'+self.kwargs['tag_url']+'/activities/'+self.kwargs['pk_activity']+'/task/'+self.kwargs['pk_task']+'/upload-file/'
		return context

	def form_valid(self, form):
		tarea = Tarea.objects.get(pk = self.kwargs['pk_task'])
		form.instance.tarea = tarea
		form_data = form.save()
		register_activity_profile_user(self.request.user, 'Archivo subido de la tarea '+tarea.nombre_tarea+' de la actividad '+tarea.actividad.nombre_actividad+' en el proyecto '+tarea.actividad.proyecto.nombre_proyecto)
		register_activity_project(self.request.user, tarea.actividad.proyecto, 'Archivo subido de la tarea '+tarea.nombre_tarea+' de la actividad '+tarea.actividad.nombre_actividad+' en el proyecto '+tarea.actividad.proyecto.nombre_proyecto)
		for users in tarea.actividad.actividad_role_set.all():
			register_notification(users.role.user, 'fa-file', 'Hay un nuevo archivo subido en la tarea <a href="/project/'+str(tarea.actividad.proyecto.pk)+'/'+tarea.actividad.proyecto.tag_url+'/activities/'+str(tarea.actividad.pk)+'/task/'+str(tarea.pk)+'/detail-task/">'+tarea.nombre_tarea+'</a> de la actividad <a href="/project/'+str(tarea.actividad.proyecto.pk)+'/'+tarea.actividad.proyecto.tag_url+'/activities/'+str(tarea.actividad.pk)+'/detail-activity/">'+tarea.actividad.nombre_actividad+'</a> del proyecto <a href="/project/'+str(tarea.actividad.proyecto.pk)+'/'+tarea.actividad.proyecto.tag_url+'/">'+tarea.actividad.proyecto.nombre_proyecto+'</a>')
		return super(UploadFileView, self).form_valid(form)

	def get_success_url(self):
		return reverse('detail_task', args = (self.kwargs['pk'], self.kwargs['tag_url'], self.kwargs['pk_activity'], self.kwargs['pk_task']))

@login_required
def delete_task(request, pk, tag_url, pk_activity, pk_task):
	response = {}
	tarea = Tarea.objects.get(pk = pk_task)
	register_activity_profile_user(request.user, 'Tarea '+tarea.nombre_tarea+' eliminada de la actividad '+tarea.actividad.nombre_actividad+' del proyecto '+tarea.actividad.proyecto.nombre_proyecto)
	register_activity_project(request.user, tarea.actividad.proyecto, 'Tarea '+tarea.nombre_tarea+' eliminada de la actividad '+tarea.actividad.nombre_actividad+' del proyecto '+tarea.actividad.proyecto.nombre_proyecto)
	for users in tarea.actividad.actividad_role_set.all():
		register_notification(users.role.user, 'fa-tasks', 'La tarea <a href="/project/'+str(tarea.actividad.proyecto.pk)+'/'+tarea.actividad.proyecto.tag_url+'/activities/'+str(tarea.actividad.pk)+'/task/'+str(tarea.pk)+'/detail-task/">'+tarea.nombre_tarea+'</a> ha sido eliminada dentro de la actividad <a href="/project/'+str(tarea.actividad.proyecto.pk)+'/'+tarea.actividad.proyecto.tag_url+'/activities/'+str(tarea.actividad.pk)+'/detail-activity/">'+tarea.actividad.nombre_actividad+'</a> del proyecto <a href="/project/'+str(tarea.actividad.proyecto.pk)+'/'+tarea.actividad.proyecto.tag_url+'/">'+tarea.actividad.proyecto.nombre_proyecto+'</a>')
	tarea.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar la tarea'
	return HttpResponse(json.dumps(response), "application/json")

@login_required
def delete_comment(request, pk, tag_url, pk_activity, pk_task, pk_comment):
	response = {}
	comment = Comentario_tarea.objects.get(pk = pk_comment)
	register_activity_profile_user(request.user, 'Comentario eliminado de la tarea '+comment.tarea.nombre_tarea+' de la actividad '+comment.tarea.actividad.nombre_actividad+' del proyecto '+comment.tarea.actividad.proyecto.nombre_proyecto)
	register_activity_project(request.user, comment.tarea.actividad.proyecto, 'Comentario eliminado de la tarea '+comment.tarea.nombre_tarea+' de la actividad '+comment.tarea.actividad.nombre_actividad+' del proyecto '+comment.tarea.actividad.proyecto.nombre_proyecto)
	register_notification(comment.usuario, 'fa-comments', 'Tu comentario ha sido eliminado en la tarea <a href="/project/'+str(comment.tarea.actividad.proyecto.pk)+'/'+comment.tarea.actividad.proyecto.tag_url+'/activities/'+str(comment.tarea.actividad.pk)+'/task/'+str(comment.tarea.pk)+'/detail-task/">'+comment.tarea.nombre_tarea+'</a> de la actividad <a href="/project/'+str(comment.tarea.actividad.proyecto.pk)+'/'+comment.tarea.actividad.proyecto.tag_url+'/activities/'+str(comment.tarea.actividad.pk)+'/detail-activity/">'+comment.tarea.actividad.nombre_actividad+'</a> del proyecto <a href="/project/'+str(comment.tarea.actividad.proyecto.pk)+'/'+comment.tarea.actividad.proyecto.tag_url+'/">'+comment.tarea.actividad.proyecto.nombre_proyecto+'</a>')
	comment.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar el comentario'
	return HttpResponse(json.dumps(response), "application/json")

@login_required
def delete_document(request, pk, tag_url, pk_activity, pk_task, pk_document):
	response = {}
	documento = Documento.objects.get(pk = pk_document)
	register_activity_profile_user(request.user, 'Archivo eliminado de la tarea '+documento.tarea.nombre_tarea+' de la actividad '+documento.tarea.actividad.nombre_actividad+' en el proyecto '+documento.tarea.actividad.proyecto.nombre_proyecto)
	register_activity_project(request.user, documento.tarea.actividad.proyecto, 'Archivo eliminado de la tarea '+documento.tarea.nombre_tarea+' de la actividad '+documento.tarea.actividad.nombre_actividad+' en el proyecto '+documento.tarea.actividad.proyecto.nombre_proyecto)
	for users in documento.tarea.actividad.actividad_role_set.all():
		register_notification(users.role.user, 'fa-file', 'El archivo '+documento.nombre_documento+' ha sido eliminado de la tarea <a href="/project/'+str(documento.tarea.actividad.proyecto.pk)+'/'+documento.tarea.actividad.proyecto.tag_url+'/activities/'+str(documento.tarea.actividad.pk)+'/task/'+str(documento.tarea.pk)+'/detail-task/">'+documento.tarea.nombre_tarea+'</a> de la actividad <a href="/project/'+str(documento.tarea.actividad.proyecto.pk)+'/'+documento.tarea.actividad.proyecto.tag_url+'/activities/'+str(documento.tarea.actividad.pk)+'/detail-activity/">'+documento.tarea.actividad.nombre_actividad+'</a> del proyecto <a href="/project/'+str(documento.tarea.actividad.proyecto.pk)+'/'+documento.tarea.actividad.proyecto.tag_url+'/">'+documento.tarea.actividad.proyecto.nombre_proyecto+'</a>')
	documento.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar el documento'
	return HttpResponse(json.dumps(response), "application/json")

@login_required
def download_document(request, pk, tag_url, pk_activity, pk_task, pk_document):
	documento = Documento.objects.get(pk = pk_document)
	register_activity_profile_user(request.user, 'Archivo descargado de la tarea '+documento.tarea.nombre_tarea+' de la actividad '+documento.tarea.actividad.nombre_actividad+' en el proyecto '+documento.tarea.actividad.proyecto.nombre_proyecto)
	register_activity_project(request.user, documento.tarea.actividad.proyecto, 'Archivo descargado de la tarea '+documento.tarea.nombre_tarea+' de la actividad '+documento.tarea.actividad.nombre_actividad+' en el proyecto '+documento.tarea.actividad.proyecto.nombre_proyecto)
	return redirect('%s/%s'%('/static/', documento.documento))

@login_required
def change_state_task(request, pk, tag_url, pk_activity, pk_task, state):
	response = {}
	if verify_user_project_administrator(pk, request.user):
		inactive = Tipo_estado.objects.get(nombre_estado = 'Terminado')
		task = Tarea.objects.get(pk = pk_task)
		if task.estado.nombre_estado == 'Terminado':
			return HttpResponseRedirect(reverse_lazy('my_list_project'))
		else:
			task.estado = inactive
			task.save()
			response['type'] = 'success'
			response['msg'] = 'Exito al finalizar la tarea'
			register_activity_profile_user(request.user, 'Tarea '+task.nombre_tarea+' de la actividad '+task.actividad.nombre_actividad+' en el proyecto '+task.actividad.proyecto.nombre_proyecto+' has sido finalizado')
			register_activity_project(request.user, task.actividad.proyecto, 'Tarea '+task.nombre_tarea+' de la actividad '+task.actividad.nombre_actividad+' en el proyecto '+task.actividad.proyecto.nombre_proyecto+' has sido finalizado')
	else:
		response['type'] = 'error'
		response['msg'] = 'Ha ocurrido un error'
	return HttpResponse(json.dumps(response), "application/json")