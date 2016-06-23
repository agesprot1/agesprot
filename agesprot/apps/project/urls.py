from django.contrib.auth.decorators import login_required
from django.conf.urls import include, patterns, url
from .views import *

role_patterns = [
	url(r'^$', list_role, name = 'list_role'),
	url(r'^add-role-project/$', add_user_project, name = 'add_user_project'),
	url(r'^delete-role-project/(?P<user>\d+)/$', delete_role_role_from_project, name = 'delete_role_role_from_project'),
]

proyect_patterns = [
	url(r'^$', login_required(DetailProjectView.as_view()), name = 'project'),
	url(r'^list-role/', include(role_patterns)),
	url(r'^update-project/$', login_required(UpdateProjectView.as_view()), name = 'update_project'),
	url(r'^delete-project/$', delete_project, name = 'delete_project'),
	url(r'^activities/', include('agesprot.apps.activity.urls')),
]

urlpatterns = patterns('agesprot.apps.project.views',
	url(r'^(?P<pk>\d+)/(?P<tag_url>[\w\-]+)/', include(proyect_patterns)),
	url(r'^new-project/$', login_required(NewProjectView.as_view()), name = 'new_project'),
	url(r'^list-project/$', login_required(ListProjectView.as_view()), name = 'list_project'),
	url(r'^my-list-project/$', login_required(ListProjectUserView.as_view()), name = 'my_list_project'),
)