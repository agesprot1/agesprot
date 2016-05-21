# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import *
from django.shortcuts import render
from .models import *
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
	model = Proyecto

	def get_context_data(self, **kwargs):
		context = super(ListProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Mis proyectos creados'
		return context

	def get_queryset(self):
		return Proyecto.objects.filter(user = self.request.user)

class DetailProjectView(DetailView):
	template_name = var_dir_template+'detail_project.html'
	model = Proyecto

	def get(self, request, **kwargs):
		self.object = self.get_object()
		if self.object.user != self.request.user:
			return HttpResponseRedirect(reverse('home'))
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_context_data(self, **kwargs):
		context = super(DetailProjectView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Proyecto '+data_project.nombre_proyecto
		return context

class ListRolesProjectView(ListView):
	template_name = var_dir_template+'list_roles_project.html'
	model = Project_role

	def get_context_data(self, **kwargs):
		context = super(ListRolesProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Lista de Roles de projectos'
		return context

@permission_required('is_staff')
def form_role(request, role_pk):
	response = {}
	try:
		role = Project_role.objects.get(pk = role_pk)
	except Project_role.DoesNotExist:
		role = role_pk
	if request.method == 'POST':
		form = RoleProjectForm(request.POST, instance = role)
		if form.is_valid():
			project_response = form.save()
			response['type'] = 'success'
			response['pk'] = project_response.pk
			response['nombre_role'] = project_response.nombre_role
			response['msg'] = 'Operación exitosa'
		else:
			response['type'] = 'error'
			response['msg'] = 'Ha ocurrido un error'
		return HttpResponse(json.dumps(response), "application/json")
	else:
		form = RoleProjectForm(instance = role)
	return render(request, var_dir_template+'form-role.html', {'forms': form, 'role': role_pk, 'title': 'Roles de proyectos'})

@permission_required('is_staff')
def delete_role(request, role_pk):
	response = {}
	try:
		role = Project_role.objects.get(pk = role_pk)
		role.delete()
		response['type'] = 'success'
		response['msg'] = 'Exito al eliminar el rol'
	except Project_role.DoesNotExist:
		response['type'] = 'error'
		response['msg'] = 'Rol no encontrado'
	return HttpResponse(json.dumps(response), "application/json")