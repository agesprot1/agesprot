from django.contrib.auth.decorators import permission_required, login_required
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('agesprot.apps.project.views',
	url(r'^(?P<pk>\d+)/$', login_required(DetailProjectView.as_view()), name = 'project'),
	url(r'^list-project/$', login_required(ListProjectView.as_view()), name = 'list_project'),
	url(r'^new-project/$', login_required(NewProjectView.as_view()), name = 'new_project'),
	url(r'^list-roles-project/$', permission_required('is_staff')(ListRolesProjectView.as_view()), name = 'list_roles_project'),
	url(r'^form-role/(?:/(?P<role_pk>\d+))?', 'form_role', name = 'form_role'),
	url(r'^delete-role/(?P<role_pk>\d+)/$', 'delete_role', name = 'delete_role'),
)