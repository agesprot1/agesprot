# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from agesprot.apps.base.models import Tipo_role
from templatetags.project_filters import *
from django.shortcuts import render
from .models import *
from .forms import *
import json

var_dir_template = 'project/'

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
		context['url'] = '/project/update-project/'+self.kwargs['pk']+'/'
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		data_object = form.save(commit = False)
		data_object.tag_url = data_object.nombre_proyecto.replace(' ', '-')
		data_object.save()
		return super(UpdateProjectView, self).form_valid(form)

class ListProjectUserView(ListView):
	template_name = var_dir_template+'list_project.html'
	model = Proyecto

	def get_context_data(self, **kwargs):
		context = super(ListProjectUserView, self).get_context_data(**kwargs)
		context['title'] = 'Mis proyectos creados'
		return context

	def get_queryset(self):
		return Proyecto.objects.filter(user = self.request.user).order_by('estado')

class ListProjectView(ListView):
	template_name = var_dir_template+'list_project.html'
	model = Proyecto

	def get_context_data(self, **kwargs):
		context = super(ListProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Lista de todos los proyectos'
		return context

	def get_queryset(self):
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

@login_required
def list_role(request, pk, tag_url):
	project = Proyecto.objects.get(pk = pk)
	list_roles = Roles_project.objects.filter(proyecto = project)
	return render(request, var_dir_template+'list_roles_project.html', {'list_roles': list_roles, 'project': project, 'title': 'Lista de roles del proyecto '+project.nombre_proyecto})

@login_required
def delete_role_role_from_project(request, user, project):
	response = {}
	verify = verify_user_project_administrator(project, request.user.pk)
	if verify is True:
		role_project = Roles_project.objects.get(user = user, proyecto = project)
		role_project.delete()
		response['type'] = 'success'
		response['msg'] = 'Exito al eliminar el usuario'
	else:
		response['type'] = 'error'
		response['msg'] = 'Ha ocurrido un error'
	return HttpResponse(json.dumps(response), "application/json")

@login_required
def add_user_project(request, project):
	project = Proyecto.objects.get(pk = project)
	if request.method == 'POST':
		response = {}
		form = AddUserProjectForm(request.POST, instance = project)
		if form.is_valid():
			project_data = form.save(commit = False)
			project_data.proyecto = project
			project_data.save()
		return HttpResponseRedirect(reverse('list_role', kwargs={'pk': project.pk, 'tag_url': project.tag_url}))
	else:
		form = AddUserProjectForm(instance = project)
	return render(request, var_dir_template+'form_add_user_project.html', {'forms': form, 'project_pk': project.pk, 'title': 'Agregar usuarios al proyecto'})

@login_required
def delete_project(request, pk):
	response = {}
	proyecto = Proyecto.objects.get(pk = pk)
	proyecto.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar el proyecto'
	return HttpResponse(json.dumps(response), "application/json")