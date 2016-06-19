# -*- encoding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView
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
		context['url'] = '/project/activities/new-activity/'+self.kwargs['pk']+'/'
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

	def get_context_data(self, **kwargs):
		context = super(UpdateActivitieView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk_project'])
		context['title'] = 'Editar actividad'
		context['project'] = data_project
		context['url'] = '/project/activities/update-activity/'+self.kwargs['pk']+'/'+self.kwargs['pk_project']+'/'
		return context

	def get_success_url(self):
		data_project = Proyecto.objects.get(pk = self.kwargs['pk_project'])
		return reverse('list_activities', args = (data_project.pk, data_project.tag_url))

@login_required
def delete_activities(request, pk):
	response = {}
	actividad = Actividad.objects.get(pk = pk)
	actividad.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar la actividad'
	return HttpResponse(json.dumps(response), "application/json")