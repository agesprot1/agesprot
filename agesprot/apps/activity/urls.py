from django.contrib.auth.decorators import login_required
from django.conf.urls import include, patterns, url
from .views import *

activity_patterns = [
	url(r'^update-activity/$', login_required(UpdateActivitieView.as_view()), name = 'update_activities'),
	url(r'^delete-activity/$', delete_activities, name = 'delete_activities'),
	url(r'^detail-activity/$', login_required(DetailActivitieView.as_view()), name = 'detail_activities'),
	url(r'^add-user-activity/$', login_required(UserRoleActivitieView.as_view()), name = 'add_user_activity'),
	url(r'^delete-user-activity/(?P<pk_role>\d+)/$', delete_user_activity, name = 'delete_user_activity'),
	url(r'^task/', include('agesprot.apps.task.urls')),
]

urlpatterns = patterns('agesprot.apps.activity.views',
	url(r'^$', login_required(ListActivitiesView.as_view()), name = 'list_activities'),
	url(r'^new-activity/$', login_required(NewActivitieView.as_view()), name = 'new_activities'),
	url(r'^(?P<pk_activity>\d+)/', include(activity_patterns)),
)