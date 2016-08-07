# -*- encoding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from agesprot.apps.notification.utils import register_notification
from agesprot.apps.project.templatetags.project_filters import *
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from agesprot.apps.base.models import Tipo_estado
from agesprot.apps.project.models import Proyecto
from django.core.urlresolvers import reverse
from agesprot.apps.audit.utils import *
from django.shortcuts import render
from .models import *
from .forms import *
import datetime
import json

var_dir_template = 'activity/'

def verify_state_activities():
	terminate = Tipo_estado.objects.get(nombre_estado = 'Terminado')
	for activity in Actividad.objects.all():
		for task in activity.tarea_set.all():
			if task.fecha_entrega < datetime.datetime.now().date():
				task.estado = terminate
				task.save()
		if activity.fecha_entrega < datetime.datetime.now().date():
			activity.estado = terminate
			activity.save()

class ListActivitiesView(ListView):
	template_name = var_dir_template+'list_activity.html'
	model = Actividad

	def get(self, request, **kwargs):
		verify = verify_user_project(self.kwargs['pk'], self.request.user)
		detail_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return super(ListActivitiesView, self).get(request, **kwargs) if verify is True else HttpResponseRedirect(reverse('RestrProject', kwargs = {'pk_project': detail_project.pk}))

	def get_context_data(self, **kwargs):
		context = super(ListActivitiesView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Lista de Actividades'
		context['project'] = data_project
		return context

	def get_queryset(self):
		verify_state_activities()
		return Actividad.objects.filter(proyecto = self.kwargs['pk']).order_by('-fecha_entrega')

class NewActivitieView(SuccessMessageMixin, CreateView):
	template_name = var_dir_template+'form_activity.html'
	success_message = 'Actividad creada con éxito.'
	form_class = ActivitieForm

	def get_context_data(self, **kwargs):
		context = super(NewActivitieView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Crear una nueva actividad'
		context['url'] = '/project/'+self.kwargs['pk']+'/'+self.kwargs['tag_url']+'/activities/new-activity/'
		context['project'] = data_project
		return context

	def form_valid(self, form):
		proyecto = Proyecto.objects.get(pk = self.kwargs['pk'])
		form.instance.proyecto = proyecto
		form.instance.estado = Tipo_estado.objects.get(nombre_estado = 'Activo')
		form_data = form.save()
		register_activity_profile_user(self.request.user, 'Actividad '+form_data.nombre_actividad+' creada en el proyecto '+proyecto.nombre_proyecto)
		register_activity_project(self.request.user, proyecto, 'Actividad '+form_data.nombre_actividad+' creada en el proyecto '+proyecto.nombre_proyecto)
		for users in proyecto.roles_project_set.all():
			register_notification(users.user, 'fa-briefcase', 'La actividad <a href="/project/'+str(proyecto.pk)+'/'+proyecto.tag_url+'/activities/'+str(form_data.pk)+'/detail-activity/">'+form_data.nombre_actividad+'</a> ha sido creada en el proyecto <a href="/project/'+str(proyecto.pk)+'/'+proyecto.tag_url+'/">'+proyecto.nombre_proyecto+'</a>')
		return super(NewActivitieView, self).form_valid(form)

	def get_success_url(self):
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return reverse('list_activities', args = (data_project.pk, data_project.tag_url))

class UpdateActivitieView(SuccessMessageMixin, UpdateView):
	model = Actividad
	template_name = var_dir_template+'form_activity.html'
	success_message = 'Actividad actualizada con éxito.'
	form_class = ActivitieForm

	def get_object(self):
		return Actividad.objects.get(pk = self.kwargs['pk_activity'])

	def get_context_data(self, **kwargs):
		context = super(UpdateActivitieView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Editar actividad'
		context['project'] = data_project
		context['url'] = '/project/'+self.kwargs['pk']+'/'+self.kwargs['tag_url']+'/activities/'+self.kwargs['pk_activity']+'/update-activity/'
		return context

	def form_valid(self, form):
		estado = Tipo_estado.objects.all()
		proyecto = Proyecto.objects.get(pk = self.kwargs['pk'])
		form.instance.proyecto = proyecto
		form.instance.estado = estado.get(nombre_estado = 'Activo') if form.cleaned_data['fecha_entrega'] >= datetime.datetime.now().date() else estado.get(nombre_estado = 'Terminado')
		form_data = form.save()
		register_activity_profile_user(self.request.user, 'Actividad '+form_data.nombre_actividad+' actualizada en el proyecto '+proyecto.nombre_proyecto)
		register_activity_project(self.request.user, proyecto, 'Actividad '+form_data.nombre_actividad+' actualizada en el proyecto '+proyecto.nombre_proyecto)
		for users in proyecto.roles_project_set.all():
			register_notification(users.user, 'fa-briefcase', 'La actividad <a href="/project/'+str(proyecto.pk)+'/'+proyecto.tag_url+'/activities/'+str(form_data.pk)+'/detail-activity/">'+form_data.nombre_actividad+'</a> ha sido actualizada en el proyecto <a href="/project/'+str(proyecto.pk)+'/'+proyecto.tag_url+'/">'+proyecto.nombre_proyecto+'</a>')
		return super(UpdateActivitieView, self).form_valid(form)

	def get_success_url(self):
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return reverse('list_activities', args = (data_project.pk, data_project.tag_url))

class DetailActivitieView(DetailView):
	template_name = var_dir_template+'detail_activity.html'
	model = Actividad

	def get(self, request, **kwargs):
		verify = verify_user_project(self.kwargs['pk'], self.request.user)
		detail_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return super(DetailActivitieView, self).get(request, **kwargs) if verify is True else HttpResponseRedirect(reverse('RestrProject', kwargs = {'pk_project': detail_project.pk}))

	def get_context_data(self, **kwargs):
		context = super(DetailActivitieView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['project'] = data_project
		context['title'] = 'Detalle de la actividad'
		return context

	def get_object(self):
		return Actividad.objects.get(pk = self.kwargs['pk_activity'])

@login_required
def delete_activities(request, pk, tag_url, pk_activity):
	response = {}
	actividad = Actividad.objects.get(pk = pk_activity)
	register_activity_profile_user(request.user, 'Actividad '+actividad.nombre_actividad+' eliminada del proyecto '+actividad.proyecto.nombre_proyecto)
	register_activity_project(request.user, actividad.proyecto, 'Actividad '+actividad.nombre_actividad+' eliminada del proyecto '+actividad.proyecto.nombre_proyecto)
	for users in actividad.proyecto.roles_project_set.all():
		register_notification(users.user, 'fa-briefcase', 'La actividad '+actividad.nombre_actividad+' ha sido elimidada del proyecto <a href="/project/'+str(actividad.proyecto.pk)+'/'+actividad.proyecto.tag_url+'/">'+actividad.proyecto.nombre_proyecto+'</a>')
	actividad.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar la actividad'
	return HttpResponse(json.dumps(response), "application/json")

class UserRoleActivitieView(SuccessMessageMixin, FormView):
	model = Actividad_role
	template_name = var_dir_template+'form_user_role.html'
	success_message = 'Usuario agreado a la actividad.'
	form_class = UserRoleForm

	def get_form_kwargs(self):
		kwargs = super(UserRoleActivitieView, self).get_form_kwargs()
		kwargs['actividad'] = self.kwargs['pk_activity']
		kwargs['proyecto'] = self.kwargs['pk']
		return kwargs

	def get_context_data(self, **kwargs):
		context = super(UserRoleActivitieView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['project'] = data_project
		context['pk_activity'] = self.kwargs['pk_activity']
		context['title'] = 'Nuevo usuario en la actividad'
		return context

	def form_valid(self, form):
		form.instance.actividad = Actividad.objects.get(pk = self.kwargs['pk_activity'])
		form_data = form.save()
		register_activity_profile_user(self.request.user, 'Usuario '+form_data.role.user.email+' agregado a la actividad '+form_data.actividad.nombre_actividad+' del proyecto '+form_data.actividad.proyecto.nombre_proyecto)
		register_activity_project(self.request.user, form_data.actividad.proyecto, 'Usuario '+form_data.role.user.email+' agregado a la actividad '+form_data.actividad.nombre_actividad+' del proyecto '+form_data.actividad.proyecto.nombre_proyecto)
		register_notification(form_data.role.user, 'fa-briefcase', 'Te han agregado a la actividad <a href="/project/'+str(form_data.actividad.proyecto.pk)+'/'+form_data.actividad.proyecto.tag_url+'/activities/'+str(form_data.actividad.pk)+'/detail-activity/">'+form_data.actividad.nombre_actividad+'</a> del proyecto <a href="/project/'+str(form_data.actividad.proyecto.pk)+'/'+form_data.actividad.proyecto.tag_url+'/">'+form_data.actividad.proyecto.nombre_proyecto+'</a>')
		return super(UserRoleActivitieView, self).form_valid(form)

	def get_success_url(self):
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return reverse('detail_activities', args = (data_project.pk, data_project.tag_url, self.kwargs['pk_activity']))

@login_required
def delete_user_activity(request, pk, tag_url, pk_activity, pk_role):
	response = {}
	actividad_role = Actividad_role.objects.get(pk = pk_role)
	register_activity_profile_user(request.user, 'Usuario '+actividad_role.role.user.email+' eliminado de la actividad '+actividad_role.actividad.nombre_actividad+' del proyecto '+actividad_role.actividad.proyecto.nombre_proyecto)
	register_activity_project(request.user, actividad_role.actividad.proyecto, 'Usuario '+actividad_role.role.user.email+' eliminado de la actividad '+actividad_role.actividad.nombre_actividad+' del proyecto '+actividad_role.actividad.proyecto.nombre_proyecto)
	register_notification(actividad_role.role.user, 'fa-briefcase', 'Has sido eliminado de la actividad <a href="/project/'+str(actividad_role.actividad.proyecto.pk)+'/'+actividad_role.actividad.proyecto.tag_url+'/activities/'+str(actividad_role.actividad.pk)+'/detail-activity/">'+actividad_role.actividad.nombre_actividad+'</a> en el proyecto <a href="/project/'+str(actividad_role.actividad.proyecto.pk)+'/'+actividad_role.actividad.proyecto.tag_url+'/">'+actividad_role.actividad.proyecto.nombre_proyecto+'</a>')
	actividad_role.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar el usuario de la actividad'
	return HttpResponse(json.dumps(response), "application/json")

@login_required
def change_state_activity(request, pk, tag_url, pk_activity, state):
	response = {}
	if verify_user_project_administrator(pk, request.user):
		inactive = Tipo_estado.objects.get(nombre_estado = 'Terminado')
		actividad = Actividad.objects.get(pk = pk_activity)
		if actividad.estado.nombre_estado == 'Terminado':
			return HttpResponseRedirect(reverse_lazy('my_list_project'))
		else:
			actividad.estado = inactive
			actividad.save()
			response['type'] = 'success'
			response['msg'] = 'Exito al finalizar la actividad'
			register_activity_profile_user(request.user, 'Actividad '+actividad.nombre_actividad+' del proyecto '+actividad.proyecto.nombre_proyecto+' ha sido finalizado')
			register_activity_project(request.user, actividad.proyecto, 'Actividad '+actividad.nombre_actividad+' del proyecto '+actividad.proyecto.nombre_proyecto+' has sido finalizado')
			for users in actividad.proyecto.roles_project_set.all():
				register_notification(users.user, 'fa-briefcase', 'La actividad <a href="/project/'+str(actividad.proyecto.pk)+'/'+actividad.proyecto.tag_url+'/activities/'+str(actividad.pk)+'/detail-activity/">'+actividad.nombre_actividad+'</a> ha sido finalizada del proyecto <a href="/project/'+str(actividad.proyecto.pk)+'/'+actividad.proyecto.tag_url+'/">'+actividad.proyecto.nombre_proyecto+'</a>')
	else:
		response['type'] = 'error'
		response['msg'] = 'Ha ocurrido un error'
	return HttpResponse(json.dumps(response), "application/json")

def response_data_activity_chart(request, pk, tag_url, pk_activity):
	response_tot = {}
	count = 0
	activity = Actividad.objects.get(pk = pk_activity)
	for task_data in activity.tarea_set.all():
		response_tot[count] = {}
		response_tot[count]['id'] = str(task_data.pk)
		response_tot[count]['name'] = task_data.nombre_tarea
		response_tot[count]['day_init'] = task_data.fecha_creacion.day
		response_tot[count]['month_init'] = task_data.fecha_creacion.month
		response_tot[count]['year_init'] = task_data.fecha_creacion.year
		response_tot[count]['day_end'] = task_data.fecha_entrega.day
		response_tot[count]['month_end'] = task_data.fecha_entrega.month
		response_tot[count]['year_end'] = task_data.fecha_entrega.year
		count += 1
	response_tot['response'] = 1 if count > 1 else 0
	return HttpResponse(json.dumps(response_tot), "application/json")