from django.contrib.auth.decorators import permission_required, login_required
from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = patterns('agesprot.apps.project.views',
	url(r'^(?P<pk>\d+)/$', login_required(DetailProjectView.as_view()), name = 'project'),
	url(r'^list-project/$', login_required(ListProjectView.as_view()), name = 'list_project'),
	url(r'^new-project/$', login_required(NewProjectView.as_view()), name = 'new_project'),
	url(r'^(?P<project>\d+)/list-role/$', 'list_role', name = 'list_role'),
	url(r'^delete-from-list-role/(?P<user>\d+)/(?P<project>\d+)/$', 'delete_role_role_from_project', name = 'delete_role_role_from_project'),
	url(r'^add-user-project/(?P<project>\d+)/$', 'add_user_project', name = 'add_user_project'),
	url(r'^(?P<pk>\d+)/tasks/', include('agesprot.apps.task.urls')),
)