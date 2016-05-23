# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from agesprot.apps.base.models import Tipo_role
from django.views.generic.list import ListView
from django.views.generic.edit import *
from django.shortcuts import render
from .models import *
from .utils import *
from .forms import *
import json

var_dir_template = 'project/'

class NewProjectView(FormView):
	template_name = var_dir_template+'form-project.html'
	success_url = reverse_lazy('list_project')
	form_class = ProjectForm

	def get_context_data(self, **kwargs):
		context = super(NewProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Crear un nuevo projecto'
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return super(NewProjectView, self).form_valid(form)

class ListProjectView(ListView):
	template_name = var_dir_template+'list_project.html'
	paginate_by = 6
	model = Proyecto

	def get_context_data(self, **kwargs):
		context = super(ListProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Mis proyectos creados'
		return context

	def get_queryset(self):
		return Proyecto.objects.filter(user = self.request.user).order_by('estado')

class DetailProjectView(DetailView):
	template_name = var_dir_template+'detail_project.html'
	model = Proyecto

	def get(self, request, **kwargs):
		self.object = self.get_object()
		verify = verify_user_project(self.object.pk, self.request.user)
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context) if verify is True else HttpResponseRedirect(reverse('home'))

	def get_context_data(self, **kwargs):
		context = super(DetailProjectView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Proyecto '+data_project.nombre_proyecto
		context['project'] = data_project
		return context

@login_required
def list_role(request, project):
	project = Proyecto.objects.get(pk = project)
	list_roles = Roles_project.objects.filter(proyecto = project)
	verify = verify_user_project_administrator(project.pk, request.user.pk)
	return render(request, var_dir_template+'list_roles_project.html', {'list_roles': list_roles, 'project': project, 'title': 'Lista de roles del proyecto '+project.nombre_proyecto}) if verify is True else HttpResponseRedirect(reverse('home'))

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
			response['user'] = project_data.user.first_name+" "+project_data.user.last_name
			response['pk_user'] = project_data.user.pk
			response['pk_project'] = project_data.proyecto.pk
			response['role'] = project_data.role.nombre_role
			response['pk'] = project_data.pk
			response['type'] = 'success'
			response['msg'] = 'Exito al agregar el usuario'
		else:
			response['type'] = 'error'
			response['msg'] = 'Ha ocurrido un error'
		return HttpResponse(json.dumps(response), "application/json")
	else:
		form = AddUserProjectForm(instance = project)
	return render(request, var_dir_template+'add_user_project.html', {'forms': form, 'project_pk': project.pk, 'title': 'Agregar usuarios al proyecto'})