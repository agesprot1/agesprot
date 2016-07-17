# -*- encoding: utf-8 -*-
from agesprot.apps.audit.register_activity import register_activity_profile_user
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from agesprot.apps.base.models import Tipo_role, Tipo_estado
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from templatetags.project_filters import *
from django.shortcuts import render
from .models import *
from .forms import *
import datetime
import json

var_dir_template = 'project/'

def verify_state_project():
	terminate = Tipo_estado.objects.get(nombre_estado = 'Terminado')
	for project in Proyecto.objects.all():
		if project.fecha_final < datetime.datetime.now().date():
			project.estado = terminate
			project.save()

class NewProjectView(SuccessMessageMixin, CreateView):
	template_name = var_dir_template+'form_project.html'
	success_url = reverse_lazy('my_list_project')
	success_message = 'Proyecto creado con exito.'
	form_class = ProjectForm

	def get_context_data(self, **kwargs):
		context = super(NewProjectView, self).get_context_data(**kwargs)
		context['url'] = '/project/new-project/'
		context['title'] = 'Crear un nuevo proyecto'
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		data_object = form.save(commit = False)
		data_object.tag_url = data_object.nombre_proyecto.replace(' ', '-')
		data_object.save()
		role = Tipo_role.objects.get(nombre_role = "Administrador")
		project_role = Roles_project(user = self.request.user, proyecto = data_object, role = role)
		project_role.save()
		register_activity_profile_user(self.request.user, 'Proyecto '+data_object.nombre_proyecto+' creado')
		return super(NewProjectView, self).form_valid(form)

class UpdateProjectView(SuccessMessageMixin, UpdateView):
	template_name = var_dir_template+'form_project.html'
	success_url = reverse_lazy('my_list_project')
	success_message = 'Proyecto actualizado con exito.'
	form_class = ProjectForm
	model = Proyecto

	def get_context_data(self, **kwargs):
		context = super(UpdateProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Editar proyecto'
		context['url'] = '/project/'+self.kwargs['pk']+'/'+self.kwargs['tag_url']+'/update-project/'
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		data_object = form.save(commit = False)
		data_object.tag_url = data_object.nombre_proyecto.replace(' ', '-')
		data_object.save()
		register_activity_profile_user(self.request.user, 'Proyecto '+data_object.nombre_proyecto+' editado. Code: '+str(data_object.pk))
		return super(UpdateProjectView, self).form_valid(form)

class ListProjectUserView(ListView):
	template_name = var_dir_template+'list_project.html'
	model = Proyecto

	def get_context_data(self, **kwargs):
		context = super(ListProjectUserView, self).get_context_data(**kwargs)
		context['title'] = 'Mis proyectos creados'
		return context

	def get_queryset(self):
		verify_state_project()
		return Proyecto.objects.filter(user = self.request.user).order_by('estado')

class ListProjectView(ListView):
	template_name = var_dir_template+'list_project.html'
	model = Proyecto

	def get_context_data(self, **kwargs):
		context = super(ListProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Lista de todos los proyectos'
		return context

	def get_queryset(self):
		verify_state_project()
		queryset = Proyecto.objects.exclude(user = self.request.user).order_by('estado')
		return queryset

class DetailProjectView(DetailView):
	template_name = var_dir_template+'detail_project.html'
	model = Proyecto

	def get(self, request, **kwargs):
		self.object = self.get_object()
		verify = verify_user_project(self.object.pk, self.request.user)
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context) if verify is True else HttpResponseRedirect(reverse('dashboard'))

	def get_context_data(self, **kwargs):
		context = super(DetailProjectView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Proyecto '+data_project.nombre_proyecto
		context['project'] = data_project
		return context

class AuditProjectView(DetailView):
	template_name = var_dir_template+'audit_project.html'
	model = Proyecto

	def get(self, request, **kwargs):
		self.object = self.get_object()
		verify = verify_user_project_administrator(self.object.pk, self.request.user)
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context) if verify is True else HttpResponseRedirect(reverse('dashboard'))

	def get_context_data(self, **kwargs):
		context = super(AuditProjectView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Auditoria el proyecto '+data_project.nombre_proyecto
		context['project'] = data_project
		return context

@login_required
def list_role(request, pk, tag_url):
	project = Proyecto.objects.get(pk = pk)
	list_roles = Roles_project.objects.filter(proyecto = project)
	return render(request, var_dir_template+'list_roles_project.html', {'list_roles': list_roles, 'project': project, 'title': 'Lista de roles del proyecto '+project.nombre_proyecto})

@login_required
def delete_project(request, pk, tag_url):
	response = {}
	proyecto = Proyecto.objects.get(pk = pk)
	register_activity_profile_user(request.user, 'Proyecto '+proyecto.nombre_proyecto+' eliminado')
	proyecto.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar el proyecto'
	return HttpResponse(json.dumps(response), "application/json")

@login_required
def delete_role_role_from_project(request, pk, tag_url, user):
	response = {}
	verify = verify_user_project_administrator(pk, request.user.pk)
	if verify is True:
		role_project = Roles_project.objects.get(user = user, proyecto = pk)
		register_activity_profile_user(request.user, 'Usuario '+role_project.user.email+' eliminado del proyecto '+role_project.proyecto.nombre_proyecto)
		role_project.delete()
		response['type'] = 'success'
		response['msg'] = 'Exito al eliminar el usuario'
	else:
		response['type'] = 'error'
		response['msg'] = 'Ha ocurrido un error'
	return HttpResponse(json.dumps(response), "application/json")

@login_required
def add_user_project(request, pk, tag_url):
	project = Proyecto.objects.get(pk = pk, tag_url = tag_url)
	if request.method == 'POST':
		response = {}
		form = AddUserProjectForm(request.POST, instance = project)
		if form.is_valid():
			project_data = form.save(commit = False)
			register_activity_profile_user(request.user, 'Usuario '+project_data.user.email+' agregado al proyecto '+project.nombre_proyecto)
			project_data.proyecto = project
			project_data.save()
		return HttpResponseRedirect(reverse('list_role', kwargs={'pk': project.pk, 'tag_url': project.tag_url}))
	else:
		form = AddUserProjectForm(instance = project)
	return render(request, var_dir_template+'form_add_user_project.html', {'forms': form, 'project': project, 'title': 'Agregar usuarios al proyecto'})

def response_data_project_chart(request, pk, tag_url):
	response_tot = {}
	count = 0
	project = Proyecto.objects.get(pk = pk)
	for activity_data in project.actividad_set.all():
		response_tot[count] = {}
		response_tot[count]['id'] = str(activity_data.pk)
		response_tot[count]['name'] = activity_data.nombre_actividad
		response_tot[count]['day_init'] = activity_data.fecha_creacion.day
		response_tot[count]['month_init'] = activity_data.fecha_creacion.month
		response_tot[count]['year_init'] = activity_data.fecha_creacion.year
		response_tot[count]['day_end'] = activity_data.fecha_entrega.day
		response_tot[count]['month_end'] = activity_data.fecha_entrega.month
		response_tot[count]['year_end'] = activity_data.fecha_entrega.year
		response_tot[count]['percent'] = percent_activity(activity_data)
		count += 1
	response_tot['response'] = 1 if count > 1 else 0
	return HttpResponse(json.dumps(response_tot), "application/json")

def percent_activity(activity_pk):
	state_terminate = Tipo_estado.objects.get(nombre_estado = 'Terminado')
	activity_tot = activity_pk.tarea_set.all().count()
	activity_terminate = activity_pk.tarea_set.filter(estado = state_terminate).count()
	return regla_tres(activity_terminate, activity_tot) if activity_tot != 0 else 0