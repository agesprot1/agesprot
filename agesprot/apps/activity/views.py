# -*- encoding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from agesprot.apps.project.models import Proyecto
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
import json

var_dir_template = 'activity/'

class ListActivitiesView(ListView):
	template_name = var_dir_template+'list_activity.html'
	model = Actividad

	def get_context_data(self, **kwargs):
		context = super(ListActivitiesView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Lista de Actividades'
		context['project'] = data_project
		return context

	def get_queryset(self):
		return Actividad.objects.filter(proyecto = self.kwargs['pk']).order_by('nombre_actividad')

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
		form.instance.proyecto = Proyecto.objects.get(pk = self.kwargs['pk'])
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

	def get_success_url(self):
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return reverse('list_activities', args = (data_project.pk, data_project.tag_url))

class DetailActivitieView(DetailView):
	template_name = var_dir_template+'detail_activity.html'
	model = Actividad

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
		form.save()
		return super(UserRoleActivitieView, self).form_valid(form)

	def get_success_url(self):
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return reverse('detail_activities', args = (data_project.pk, data_project.tag_url, self.kwargs['pk_activity']))

@login_required
def delete_user_activity(request, pk, tag_url, pk_activity, pk_role):
	response = {}
	actividad_role = Actividad_role.objects.get(pk = pk_role)
	actividad_role.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar el usuario de la actividad'
	return HttpResponse(json.dumps(response), "application/json")