from django.contrib.auth.decorators import login_required
from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = patterns('agesprot.apps.project.views',
	url(r'^(?P<pk>\d+)/(?P<tag_url>.+)/$', login_required(DetailProjectView.as_view()), name = 'project'),
	url(r'^list-project/$', login_required(ListProjectView.as_view()), name = 'list_project'),
	url(r'^my-list-project/$', login_required(ListProjectUserView.as_view()), name = 'my_list_project'),
	url(r'^new-project/$', login_required(NewProjectView.as_view()), name = 'new_project'),
	url(r'^update-project/(?P<pk>\d+)/$', login_required(UpdateProjectView.as_view()), name = 'update_project'),
	url(r'^delete-project/(?P<pk>\d+)/$', 'delete_project', name = 'delete_project'),
	url(r'^list-role(?P<pk>\d+)/(?P<tag_url>.+)/$', 'list_role', name = 'list_role'),
	url(r'^delete-from-list-role/(?P<user>\d+)/(?P<project>\d+)/$', 'delete_role_role_from_project', name = 'delete_role_role_from_project'),
	url(r'^add-user-project/(?P<project>\d+)/$', 'add_user_project', name = 'add_user_project'),
	url(r'^activities/', include('agesprot.apps.activity.urls')),
)