from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from .views import *

login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/dashboard/')

urlpatterns = patterns('agesprot.apps.base.views',
	url(r'^$', login_forbidden(TemplateView.as_view(template_name = 'home/landing.html')), {'title': 'Inicio'}, name = 'landing'),
	url(r'^dashboard/$', login_required(TemplateView.as_view(template_name = 'home/dashboard.html')), {'title': 'Bienvenio'}, name = 'dashboard'),
	url(r'^list-roles-project/$', permission_required('is_staff')(ListRolesProjectView.as_view()), name = 'list_roles_project'),
	url(r'^form-role/(?:/(?P<role_pk>\d+))?', 'form_role', name = 'form_role'),
	url(r'^delete-role/(?P<role_pk>\d+)/$', 'delete_role', name = 'delete_role'),
	url(r'^list-prioridad-project/$', permission_required('is_staff')(ListPrioridadProjectView.as_view()), name = 'list_prioridad_project'),
	url(r'^form-prioridad/(?:/(?P<prioridad_pk>\d+))?', 'form_prioridad', name = 'form_prioridad'),
	url(r'^delete-prioridad/(?P<prioridad_pk>\d+)/$', 'delete_prioridad', name = 'delete_prioridad'),
)