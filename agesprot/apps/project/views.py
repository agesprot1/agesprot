# -*- encoding: utf-8 -*-
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView, FormView
from django.contrib.auth.decorators import permission_required, login_required
from agesprot.apps.notification.utils import register_notification
from django.contrib.messages.views import SuccessMessageMixin
from agesprot.apps.base.models import Tipo_role, Tipo_estado
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from templatetags.project_filters import *
from agesprot.apps.audit.utils import *
from agesprot.apps.base.emails import *
from django.shortcuts import render
from .models import *
from .forms import *
import datetime
import json

var_dir_template = 'project/'

def verify_state_project():
	terminate = Tipo_estado.objects.get(nombre_estado = 'Terminado')
	for proyecto in Proyecto.objects.all():
		if proyecto.fecha_final < datetime.datetime.now().date():
			proyecto.estado = terminate
			proyecto.save()
			for users in proyecto.roles_project_set.all():
				register_notification(users.user, 'fa-folder', 'El proyecto '+proyecto.nombre_proyecto+' ha sido finalizado automaticamente')

class RestrictionProjectView(TemplateView):
	template_name = var_dir_template+'restriction_project.html'

	def get_context_data(self, **kwargs):
		context = super(RestrictionProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Error de Acceso'
		context['pk_project'] = Proyecto.objects.get(pk = self.kwargs['pk_project'])
		return context

class NewProjectView(SuccessMessageMixin, CreateView):
	template_name = var_dir_template+'form_project.html'
	success_url = reverse_lazy('my_list_project')
	success_message = 'Proyecto creado con exito.'
	form_class = ProjectForm

	def get_context_data(self, **kwargs):
		context = super(NewProjectView, self).get_context_data(**kwargs)
		context['type_request'] = 'create'
		context['url'] = '/project/new-project/'
		context['title'] = 'Crear un nuevo proyecto'
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		data_object = form.save()
		role = Tipo_role.objects.get(nombre_role = "Administrador")
		project_role = Roles_project(user = self.request.user, proyecto = data_object, role = role)
		project_role.save()
		register_activity_profile_user(self.request.user, 'Proyecto '+data_object.nombre_proyecto+' creado')
		register_activity_project(self.request.user, data_object, 'Proyecto '+data_object.nombre_proyecto+' creado')
		register_notification(self.request.user, 'fa-folder', 'El proyecto <a href="/project/'+str(data_object.pk)+'/'+data_object.tag_url+'/">'+data_object.nombre_proyecto+'</a> ha sido creado con exito.')
		return super(NewProjectView, self).form_valid(form)

class UpdateProjectView(SuccessMessageMixin, UpdateView):
	template_name = var_dir_template+'form_project.html'
	success_url = reverse_lazy('my_list_project')
	success_message = 'Proyecto actualizado con exito.'
	form_class = ProjectForm
	model = Proyecto

	def get_context_data(self, **kwargs):
		context = super(UpdateProjectView, self).get_context_data(**kwargs)
		context['type_request'] = 'update'
		context['title'] = 'Editar proyecto'
		context['url'] = '/project/'+self.kwargs['pk']+'/'+self.kwargs['tag_url']+'/update-project/'
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		data_object = form.save()
		register_activity_profile_user(self.request.user, 'Proyecto '+data_object.nombre_proyecto+' editado.')
		register_activity_project(self.request.user, data_object, 'Proyecto '+data_object.nombre_proyecto+' editado. Code: '+str(data_object.pk))
		for users in data_object.roles_project_set.all():
			register_notification(users.user, 'fa-folder', 'El proyecto <a href="/project/'+str(data_object.pk)+'/'+data_object.tag_url+'/">'+data_object.nombre_proyecto+'</a> ha sido editado por '+self.request.user.email)
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
		detail_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return self.render_to_response(context) if verify is True else HttpResponseRedirect(reverse('RestrProject', kwargs = {'pk_project': detail_project.pk}))

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
		detail_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return self.render_to_response(context) if verify is True else HttpResponseRedirect(reverse('RestrProject', kwargs = {'pk_project': detail_project.pk}))

	def get_context_data(self, **kwargs):
		context = super(AuditProjectView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Auditoria el proyecto '+data_project.nombre_proyecto
		context['project'] = data_project
		return context

class InvitationProjectView(SuccessMessageMixin, CreateView):
	template_name = var_dir_template+'invitation_project_form.html'
	success_message = 'Invitación enviada con éxito'
	form_class = InvitationProjectForm

	def get_form_kwargs(self):
		kwargs = super(InvitationProjectView, self).get_form_kwargs()
		kwargs['email'] = self.request.GET.get('email')
		return kwargs

	def get_context_data(self, **kwargs):
		context = super(InvitationProjectView, self).get_context_data(**kwargs)
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		context['title'] = 'Enviar invitación'
		context['project'] = data_project
		return context

	def form_valid(self, form):
		proyecto = Proyecto.objects.get(pk = self.kwargs['pk'])
		form.instance.proyecto = proyecto
		data_object = form.save()
		app_send_email_invitate(data_object.email, self.request.META['HTTP_HOST'], u'Invitación al proyecto '+proyecto.nombre_proyecto, 'email/project_invitate_user.html', data_object)
		register_activity_project(self.request.user, data_object, 'Invitacion enviada al email '+data_object.email)
		return super(InvitationProjectView, self).form_valid(form)

	def get_success_url(self):
		data_project = Proyecto.objects.get(pk = self.kwargs['pk'])
		return reverse('list_role', args = (data_project.pk, data_project.tag_url))

@login_required
def list_role(request, pk, tag_url):
	project = Proyecto.objects.get(pk = pk)
	list_roles = Roles_project.objects.filter(proyecto = project)
	verify = verify_user_project(project.pk, request.user)
	return render(request, var_dir_template+'list_roles_project.html', {'list_roles': list_roles, 'project': project, 'title': 'Lista de roles del proyecto '+project.nombre_proyecto}) if verify is True else HttpResponseRedirect(reverse('RestrProject', kwargs = {'pk_project': project.pk}))

@login_required
def delete_project(request, pk, tag_url):
	response = {}
	proyecto = Proyecto.objects.get(pk = pk)
	register_activity_profile_user(request.user, 'Proyecto '+proyecto.nombre_proyecto+' eliminado')
	for users in proyecto.roles_project_set.all():
		register_notification(users.user, 'fa-folder', 'El proyecto '+proyecto.nombre_proyecto+' ha sido eliminado por '+request.user.email)
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
		register_activity_project(request.user, role_project.proyecto, 'Usuario '+role_project.user.email+' eliminado del proyecto '+role_project.proyecto.nombre_proyecto)
		register_notification(request.META['HTTP_HOST'], role_project.user, 'fa-users', 'El administrador '+request.user.email+' te ha eliminado al proyecto <a href="/project/'+str(role_project.proyecto.pk)+'/'+role_project.proyecto.tag_url+'/">'+role_project.proyecto.nombre_proyecto+'</a>')
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
			project_data.proyecto = project
			project_data.save()
			app_send_email(project_data.user, request.META['HTTP_HOST'], 'Proyecto '+project.nombre_proyecto, 'email/project_add_user.html', project)
			register_activity_profile_user(request.user, 'Usuario '+project_data.user.email+' agregado al proyecto '+project.nombre_proyecto)
			register_activity_project(request.user, project, 'Usuario '+project_data.user.email+' agregado al proyecto '+project.nombre_proyecto)
			register_notification(request.META['HTTP_HOST'], project_data.user, 'fa-users', 'El administrador '+request.user.email+' te ha agregado al proyecto <a href="/project/'+str(project.pk)+'/'+project.tag_url+'/">'+project.nombre_proyecto+'</a>')
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

def verify_project(request, tag_url, type_request):
	response = {}
	count_project = Proyecto.objects.filter(tag_url = tag_url, user = request.user.pk).count()
	response['response'] = 1 if count_project >= 1 and type_request == 'create' or count_project > 1 and type_request == 'update' else 0
	return HttpResponse(json.dumps(response), "application/json")